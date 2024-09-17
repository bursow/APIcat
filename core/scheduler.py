from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
from .api_client import async_request_handler
import logging

def schedule_requests(url, method, interval):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.run(async_request_handler(url, method)), 'interval', seconds=interval)
    scheduler.start()
    logging.info("Zamanlanmış görev başlatıldı.")
