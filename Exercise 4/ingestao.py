# %%
# Built in python abstract class
from abc import ABC, abstractmethod

from schedule import *
import json
from backoff import on_exception, expo
import requests
import ratelimit
import logging
from datetime import datetime, date, timedelta
from typing import Union

# %%
import logging
import os
# Color number definition
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# These are the sequences need to get colored output
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': RED,
    'ERROR': RED
}

# Special function used to ease a message formatting edition


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace(
            "$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

# Format log level name color accordinly


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (
                30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

# Logger class used in all logging operations


class log(logging.Logger):
	# Message format with collors \033[1;35m = Magenta
	FORMAT = '\033[35m%(asctime)s\033[0m [$BOLD%(levelname)-18s$RESET]\033[35m [%(processName)s][%(threadName)s][%(module)s]\033[0m %(message)s - $BOLDLine:%(lineno)d$RESET'
	COLOR_FORMAT = formatter_message(FORMAT, True)

	def __init__(self, name='my_logger'):
		# Create logger with debug level
		logging.Logger.__init__(self, name, logging.DEBUG)

		# create console handler and set level to debug
		if not self.handlers:
			color_formatter = ColoredFormatter(self.COLOR_FORMAT)
			ch = logging.StreamHandler()
			ch.setLevel(logging.DEBUG)
			# add formatter to ch
			ch.setFormatter(color_formatter)
			# add ch to logger
			self.addHandler(ch)

			os.makedirs('logs', exist_ok=True)
			log_file = logging.FileHandler(
				filename=os.getcwd()+f'/logs/{name}.log', mode='w+', encoding='utf8')
			formatter = logging.Formatter(
				'%(asctime)s [%(levelname)-18s][%(processName)s][%(threadName)s][%(module)s] %(message)s - %(lineno)d')
			log_file.setFormatter(formatter)
			log_file.setLevel(logging.DEBUG)
			self.addHandler(log_file)


# %%
logger = log('ingestao')

# %% [markdown]
# Tests access to the API

# %%
print(requests.get("https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/21").json())

# %% [markdown]
# Creates an abstract class for the API

# %%
class MercadoBitcoinApi(ABC):

	def __init__(self, coin: str) -> None:
		self.coin = coin
		self.base_endpoint = "https://www.mercadobitcoin.net/api"

	@abstractmethod
	def _get_endpoint(self, **kargs) -> str:
		pass


	#Ratelimit limits the amount of times the request was made in a period of time
	@on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
	@ratelimit.limits(calls=29, period=30)
	@on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
	def get_data(self, **kargs) -> dict:
		'''
			Get data form an endpoint
			Raises HTTPError exception if reponse failed
			:return dict: dictionary from endpoint json response
		'''
		endpoint = self._get_endpoint(**kargs)
		logger.info(f"Getting data from endpoint: {endpoint}")
		response = requests.get(endpoint)
		response.raise_for_status()
		return response.json()


# %% [markdown]
# Creates a derived class from the abstract class just to access the day-summary

# %%
class DaySummaryApi(MercadoBitcoinApi):
    type = "day-summary"

    def _get_endpoint(self, date: datetime.date) -> str:
        '''
            Returns endpoint for coin day summary.
        '''
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"

# %%
print(DaySummaryApi(coin="BTC").get_data(date=date(2021,6,21)))

# %% [markdown]
# Creates a derived class to get coin transactions

# %%
class TradesApi(MercadoBitcoinApi):
    type = "trades"

    def _get_unix_epoch(self, date: datetime) -> int:
        '''
            Gets unix timestamp from date
        '''
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime = None, date_to: datetime = None) -> str:
        '''
            Gets endpoint for trades in a range of time or last 1000 transactions if no argument is given
        '''
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        elif date_from and date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"

        return endpoint

# %% [markdown]
# Tests getting data from trades

# %%
TradesApi(coin="BTC").get_data()
TradesApi(coin="BTC").get_data(date_from=datetime(2021, 6, 2))
TradesApi(coin="BTC").get_data(date_from=datetime(2021, 6, 2), date_to=datetime(2021, 6, 3))

# %%
class DataTypeNotSupportedForIngestionException(Exception):
	def __init__(self, data) -> None:
		self.data = data
		self.message = f"Data type {type(data)} is not supported for ingestion."
		super().__init__(self.message)

# %% [markdown]
# Now creates a class to store data in json files

# %%
class DataWriter():

	def __init__(self, coin: str, api: str) -> None:
		self.api = api
		self.coin = coin
		self.filename = f"{self.api}/{self.coin}/{datetime.now().strftime('/%Y/%m/%d')}.json"

	def _write_row(self, row: str) -> None:
		'''
			Writes a row into the file
		'''
		os.makedirs(os.path.dirname(self.filename), exist_ok=True)
		with open(self.filename, "a") as file:
			file.write(row)

	def write(self, data: Union[list, dict]):
		'''
			Writes a list of dictionaries or a dictionary into the file
		'''
		if isinstance(data, dict):
			self._write_row(json.dumps(data) + "\n")
		elif isinstance(data, list):
			for element in data:
				# Recursion here is a good pratice to reduce code
				self.write(element)
		else:
			raise DataTypeNotSupportedForIngestionException(data)

# %%
class DataIngestor(ABC):

	def __init__(self, writer: DataWriter, coins: list[str], default_start_date: date) -> None:
		self.coins = coins
		self.default_start_date = default_start_date
		self.writer = writer
		self._checkpoint = self._load_checkpoint()
		super().__init__()

	@property
	def _checkpoint_filename(self) -> str:
		return f"{self.__class__.__name__}.checkpoint"

	def _write_checkpoint(self) -> None:
		with open(self._checkpoint_filename, 'w') as f:
			f.write(f"{self._checkpoint}")

	def _load_checkpoint(self) -> datetime.date:
		try:
			with open(self._checkpoint_filename, 'r') as f:
				return datetime.strptime(f.read(), "%Y-%m-%d").date()
		except FileNotFoundError:
			return None

	def _get_checkpoint(self) -> datetime: 
		if not self._checkpoint:
			return self.default_start_date
		else:
			return self._checkpoint

	def _update_checkpoint(self, value: date):
		self._checkpoint = value
		self._write_checkpoint()

	@abstractmethod
	def ingest(self) -> None:
		pass

# %%
class DaySummaryIngestor(DataIngestor):

	def ingest(self) -> None:
		search_date = self._get_checkpoint()
		if search_date < date.today():
			for coin in self.coins:
				api = DaySummaryApi(coin=coin)
				data = api.get_data(date=search_date)
				self.writer(coin=coin, api=api.type).write(data)
			self._update_checkpoint(search_date + timedelta(days=1))

# %%
ingestor = DaySummaryIngestor(writer=DataWriter, coins=['BTC', 'ETH', 'LTC'], default_start_date=date(2021, 6, 1))


# %%
@repeat(every(1).seconds)
def job():
	ingestor.ingest()

# %%
while True:
	run_pending()
	time.sleep(0.3)


