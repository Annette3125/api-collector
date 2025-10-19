import schedule
import time
from get_data import main

schedule.every().day.at("18:00").do(main)  # runs and extract every day new documents
print("Schedular goes - at 6:00 pm")

while True:
    schedule.run_pending()
    time.sleep(60)
