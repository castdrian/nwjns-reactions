from pyyoutube import Api, SearchResult
from os import getenv
from time import sleep
import re
from tweepy import API, OAuth1UserHandler
from datetime import datetime, timedelta, timezone

def search_videos():
	yt = Api(api_key=getenv('google_api_key'))
	search_time = datetime.now(timezone.utc) - timedelta(minutes=15)

	results = yt.search(
    	q='pentatonix reaction',
    	parts='snippet',
   		count=25,
    	published_after=search_time.isoformat(),
    	safe_search='moderate',
    	search_type='video')

	if len(results.items) == 0:
		print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] Found no results')
		return None

	print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] Found {len(results.items)} result(s)')
	return results.items

def update_status(videos: list[SearchResult]):
	auth = OAuth1UserHandler(getenv('consumer_key'), getenv('consumer_secret'), getenv('token'), getenv('secret'))
	twitter = API(auth)

	print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] Updating Twitter status')

	for video in videos:
		if is_false_positive(video):
			print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] Skipping false positive')
			continue

		twitter.update_status(f'Found new reaction: "{escape_formatting(video.snippet.title)}" by {video.snippet.channelTitle}\n#PTX #Pentatonix\nhttps://youtu.be/{video.id.videoId}')
		if len(videos) > 1: sleep(5)

	print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] Status updated')

def is_false_positive(video: SearchResult):
	if any(re.findall(r'ptx|pentatonix', video.snippet.title, re.IGNORECASE)):
		print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] Verified result')
		return False
	else:
		print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] Identified false positive')
		return True

def escape_formatting(text: str):
	return text.replace("&quot;", "\"").replace("&amp;", "&").replace("&#39;", "'")