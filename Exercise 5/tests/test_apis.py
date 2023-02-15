import datetime
import pytest
from apis import DaySummaryApi, TradesApi


class TestDaySummaryApi:
	@pytest.mark.parametrize(
		"coin, date, expected",
		[
			('BTC', datetime.date(2021, 6, 21), "https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/21"),
			('ETH', datetime.date(2021, 6, 21), "https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/21"),
			('ETH', datetime.date(2019, 1, 2), "https://www.mercadobitcoin.net/api/ETH/day-summary/2019/1/2")
		]
	)
	def test_get_endpoint(self, coin:str, date:datetime.date, expected:str):
		api = DaySummaryApi(coin=coin)
		actual = api._get_endpoint(date=date)
		assert actual == expected

class TestTradesApi:
	@pytest.mark.parametrize(
		"coin, date_from, date_to, expected",
		[
			("TEST", datetime.datetime(2019,1,1), datetime.datetime(2019,2,2), "https://www.mercadobitcoin.net/api/TEST/trades/1546311600/1549076400"),
			("TEST", datetime.datetime(2019, 6, 12), datetime.datetime(2019, 6, 15), "https://www.mercadobitcoin.net/api/TEST/trades/1560308400/1560567600"),
			("TEST", None, None, "https://www.mercadobitcoin.net/api/TEST/trades"),
			("TEST", None, datetime.datetime(2019, 6, 15), "https://www.mercadobitcoin.net/api/TEST/trades"),
			("TEST", datetime.datetime(2019, 6, 12), None, "https://www.mercadobitcoin.net/api/TEST/trades/1560308400")
		]
	)
	def test_get_endpoint(self, coin:str, date_from:datetime.date, date_to:datetime.date, expected:str):
		api = TradesApi(coin=coin)
		actual = api._get_endpoint(date_from=date_from, date_to=date_to)
		assert actual == expected
	
	def test_get_enpoint_date_from_greater_than_date_to(self):
		with pytest.raises(RuntimeError):
			actual = TradesApi(coin="TEST")._get_endpoint(date_from=datetime.datetime(2019, 6, 15), date_to=datetime.datetime(2019, 6, 12))

	@pytest.mark.parametrize(
		"date, expected",
		[
			(datetime.datetime(2019, 1, 1), 1546311600),
			(datetime.datetime(2019, 2, 2), 1549076400),
			(datetime.datetime(2019, 6, 12), 1560308400),
			(datetime.datetime(2019, 6, 12, 0, 0, 5), 1560308405),
			(datetime.datetime(2019, 6, 15), 1560567600)
		]
	)
	def test_get_unix_epoch(self, date:datetime.date, expected:int):
		actual = TradesApi(coin="TEST")._get_unix_epoch(date=date)
		assert actual == expected
