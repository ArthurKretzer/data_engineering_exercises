from abc import ABC, abstractmethod

from schedule import *
from backoff import on_exception, expo
import requests
import ratelimit
from datetime import date, datetime

from logger import log
			
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
		return int((date - datetime(1970, 1, 1)).total_seconds())

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