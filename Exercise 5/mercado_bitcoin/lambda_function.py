from ingestors import AwsDaySummaryIngestor
from writer import S3Writter
from datetime import date
from logger import log
			
logger = log('lambda_handler')

def lambda_handler(event, context):
    logger.info(f"{event}")
    logger.info(f"{context}")

    AwsDaySummaryIngestor(
		writer=S3Writter, 
		coins=['BTC', 'ETH', 'LTC'], 
		default_start_date=date(2023, 1, 1)
    ).ingest()