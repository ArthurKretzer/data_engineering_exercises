import datetime
import pytest

from unittest.mock import patch, mock_open
from mercado_bitcoin.ingestors import DataIngestor
from mercado_bitcoin.writer import DataWriter

@pytest.fixture
# Overwrites abstract methods.
@patch("mercado_bitcoin.ingestors.DataIngestor.__abstractmethods__", set())
def data_ingestor_fixture():
	return DataIngestor(
			writer=DataWriter,
			coins=["TEST", "HOW"],
			default_start_date=datetime.date(2021, 6, 21)
		)

class TestIngestors:
	def test_checkpoint_filename(self, data_ingestor_fixture):
		actual = data_ingestor_fixture._checkpoint_filename

		expected = "DataIngestor.checkpoint"

		assert actual == expected

	def test_load_checkpoint_no_checkpoint(self, data_ingestor_fixture):
		actual = data_ingestor_fixture._load_checkpoint()
		
		expected = datetime.date(2021, 6, 21)

		assert actual == expected

	# Mock needs to be inserted as a function input. Even if it is not used. 
	# This is a mock for file opening.
	@patch("builtins.open", new_callable=mock_open, read_data="2021-06-25")
	def test_load_checkpoint_existing_checkpoint(self, mock, data_ingestor_fixture):
		actual = data_ingestor_fixture._load_checkpoint() 
		
		expected = datetime.date(2021, 6, 25)

		assert actual == expected

	# Mocks the write checkpoint function to return None. Otherwise it will create a new file.
	@patch("mercado_bitcoin.ingestors.DataIngestor._write_checkpoint", return_value=None)
	def test_update_checkpoint_checkpoint_updated(self, mock, data_ingestor_fixture):
		data_ingestor = data_ingestor_fixture
		data_ingestor._update_checkpoint(datetime.date(2019, 1, 1)) 
		actual = data_ingestor._checkpoint
		expected = datetime.date(2019, 1, 1)

		assert actual == expected

	@patch("mercado_bitcoin.ingestors.DataIngestor._write_checkpoint", return_value=None)
	def test_update_checkpoint_checkpoint_written(self, mock, data_ingestor_fixture):
		data_ingestor = data_ingestor_fixture
		data_ingestor._update_checkpoint(datetime.date(2019, 1, 1)) 
		# Since mock is called in _write_checkpoint, then checks if it was called.
		mock.assert_called_once()

	@patch("builtins.open", new_callable=mock_open, read_data="2021-06-25")
	# Creates a mock to emulate filename.
	@patch("mercado_bitcoin.ingestors.DataIngestor._checkpoint_filename", return_value="foobar.checkpoint")
	# When more than one mock is created, then you need to input more mocks into the function.
	# The order is first in -> last input
	def test_write_checkpoint(self, mock_checkpoint_filename, mock_open_file, data_ingestor_fixture):
		data_ingestor = data_ingestor_fixture
		data_ingestor._write_checkpoint()
		mock_open_file.assert_called_with(mock_checkpoint_filename, 'w')