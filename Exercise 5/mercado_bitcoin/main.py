import time
from datetime import date
from schedule import repeat, every, run_pending
from ingestors import AwsDaySummaryIngestor
from writer import S3Writter

import dotenv
dotenv.load_dotenv()

if __name__ == "__main__":
	day_summary_ingestor = AwsDaySummaryIngestor(
		writer=S3Writter, 
		coins=['BTC', 'ETH', 'LTC'], 
		default_start_date=date(2023, 1, 1)
		)

	@repeat(every(1).seconds)
	def job():
		day_summary_ingestor.ingest()

	while True:
		run_pending()
		time.sleep(0.5)
