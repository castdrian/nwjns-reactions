from dotenv import load_dotenv
from util import log, search_videos, update_status
from schedule import every, run_pending
from time import sleep

load_dotenv()
log('Application initialized')

def cycle():
	log('Starting search cycle')
	videos = search_videos()
	if videos != None: update_status(videos)

	log('Cycle complete')

# Schedule cycle every quarter hour
every().hour.at(":00").do(cycle)
every().hour.at(":15").do(cycle)
every().hour.at(":30").do(cycle)
every().hour.at(":45").do(cycle)

while True:
	try:
		run_pending()
		sleep(1)
	except Exception as e:
		log('Error: ' + str(e))
