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

# Initial cycle
log('Starting initial cycle')
cycle()

# Schedule cycle
every(15).minutes.do(cycle)

while True:
	try:
		run_pending()
		sleep(1)
	except Exception as e:
		log('Error: ' + str(e))
