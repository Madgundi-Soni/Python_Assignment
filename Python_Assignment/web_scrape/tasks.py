
from celery import shared_task
from .coinmarketcap import CoinMarketCap

@shared_task
def scrape_coin(coin,job_id):
    scraper = CoinMarketCap(coin,job_id)
    return scraper.scrape_data()