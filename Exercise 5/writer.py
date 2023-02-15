from datetime import datetime
import json
import os
from typing import Union

class DataTypeNotSupportedForIngestionException(Exception):
	def __init__(self, data) -> None:
		self.data = data
		self.message = f"Data type {type(data)} is not supported for ingestion."
		super().__init__(self.message)

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