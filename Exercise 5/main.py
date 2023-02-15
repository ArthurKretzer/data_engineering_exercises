import time
from datetime import date
from schedule import repeat, every, run_pending
from ingestors import DaySummaryIngestor
from writer import DataWriter

if __name__ == "__main__":
	day_summary_ingestor = DaySummaryIngestor(
		writer=DataWriter, 
		coins=['BTC', 'ETH', 'LTC'], 
		default_start_date=date(2021, 6, 1)
		)

	trades_ingestor = TradesIngestor()

	@repeat(every(1).seconds)
	def job():
		day_summary_ingestor.ingest()

	while True:
		run_pending()
		time.sleep(0.5)
