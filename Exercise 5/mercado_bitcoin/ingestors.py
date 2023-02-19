from abc import ABC, abstractmethod

from datetime import date, datetime, timedelta
from mercado_bitcoin.writer import DataWriter
from mercado_bitcoin.apis import DaySummaryApi

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

	def _load_checkpoint(self) -> date:
		try:
			with open(self._checkpoint_filename, 'r') as f:
				return datetime.strptime(f.read(), "%Y-%m-%d").date()
		except FileNotFoundError:
			return self.default_start_date

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

class DaySummaryIngestor(DataIngestor):

	def ingest(self) -> None:
		search_date = self._get_checkpoint()
		if search_date < date.today():
			for coin in self.coins:
				api = DaySummaryApi(coin=coin)
				data = api.get_data(date=search_date)
				self.writer(coin=coin, api=api.type).write(data)
			self._update_checkpoint(search_date + timedelta(days=1))