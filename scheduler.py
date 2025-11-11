import schedule
import time
import logging
from get_data import main as run_job


logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def safe_job():
    try:
        run_job()
    except Exception as e:
        logging.exception(f"Scheduled job failed: {e}")

schedule.every().day.at("18:00").do(safe_job)  # runs and extract every day new documents
logging.info("Schedular started. Job planned at 18:00 (local time).")
print("Schedular runs daily at 18:00.")


while True:
    schedule.run_pending()
    time.sleep(60)
