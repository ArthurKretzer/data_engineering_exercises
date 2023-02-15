from abc import ABC, abstractmethod

from schedule import *
from backoff import on_exception, expo
import requests
import ratelimit
from datetime import date, datetime

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
			
logger = log('ingestao')

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

class DaySummaryApi(MercadoBitcoinApi):
	type = "day-summary"

	def _get_endpoint(self, date: date) -> str:
		'''
			Returns endpoint for coin day summary.
		'''
		return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"

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
			if date_from > date_to:
				raise RuntimeError("date_from cannot be greater than date_to")
			unix_date_from = self._get_unix_epoch(date_from)
			unix_date_to = self._get_unix_epoch(date_to)
			endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
		else:
			endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"

		return endpoint