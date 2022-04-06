from dotenv import load_dotenv
from datetime import datetime
from util import search_videos, update_status
from schedule import every, run_pending
from time import sleep

load_dotenv()
print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] Application initialized')

def cycle():
	print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] Starting search cycle')
	videos = search_videos()
	if videos != None: update_status(videos)

	print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] Cycle complete')

every(15).minutes.do(cycle)

while True:
    run_pending()
    sleep(1)