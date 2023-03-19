from datetime import datetime
import json
import os
from typing import Union
from tempfile import NamedTemporaryFile
import boto3

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

	def _write_to_file(self, data: Union[list, dict]):
		if isinstance(data, dict):
			self._write_row(json.dumps(data) + "\n")
		elif isinstance(data, list):
			for element in data:
				# Recursion here is a good pratice to reduce code
				self.write(element)
		else:
			raise DataTypeNotSupportedForIngestionException(data)

	def write(self, data: Union[list, dict]):
		'''
			Writes a list of dictionaries or a dictionary into the file
		'''
		self._write_to_file(data=data)

class S3Writter(DataWriter):
	def __init__(self, coin: str, api: str) -> None:
		super().__init__(coin, api)
		self.tempfile = NamedTemporaryFile(delete=False)
		self.client = boto3.client("s3")
		self.key = f"mercado_bitcoin/{self.api}/coin={self.coin}/extracted_at={datetime.now().date()}/{self.api}_{self.coin}_{datetime.now().strftime('/%Y/%m/%d')}.json"
	
	def _write_row(self, row: str) -> None:
		'''
			Writes a row into the file
		'''
		with open(self.tempfile.name, "a") as file:
			file.write(row)

	def write(self, data: Union[list, dict]):
		'''
			Writes a list of dictionaries or a dictionary into the file
		'''
		self._write_to_file(data=data)
		self._write_file_to_s3()

	def _write_file_to_s3(self):
		self.client.put_object(
			Body=self.tempfile,
			Bucket="solaria-data-lake-raw",
			Key=self.key
		)