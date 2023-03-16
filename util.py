from pyyoutube import Api, SearchResult
from os import getenv
from time import sleep
from re import findall, IGNORECASE
from requests import get
from tweepy import API, OAuth1UserHandler
from datetime import datetime, timedelta, timezone
from pickledb import load

def search_videos():
	yt = Api(api_key=getenv('google_api_key'))
	search_time = datetime.now(timezone.utc) - timedelta(minutes=20)

	results = yt.search(
    	q='newjeans reaction',
    	parts='snippet',
   		count=25,
    	published_after=search_time.isoformat(),
    	safe_search='moderate',
    	search_type='video')

	if len(results.items) == 0:
		log('Found no results')
		return None

	log(f'Found {len(results.items)} result(s)')
	return results.items

def update_status(videos: list[SearchResult]):
	auth = OAuth1UserHandler(getenv('consumer_key'), getenv('consumer_secret'), getenv('token'), getenv('secret'))
	twitter = API(auth)

	log('Updating Twitter status')

	for video in videos:
		if is_false_positive(video):
			log('Skipping false positive')
			continue

		if is_duplicate(video):
			log('Skipping duplicate')
			continue

		twitter.update_status(f'Found new reaction: "{escape_formatting(video.snippet.title)}" by {resolve_twitter_handle(video.snippet.channelId, video.snippet.channelTitle)}\n#NewJeans #뉴진스\n#HANNI #HAERIN #MINJI #DANIELLE #HYEIN\n#하니 #해린 #민지 #다니엘 #혜인\nhttps://youtu.be/{video.id.videoId}')
		if len(videos) > 1: sleep(5)

	log('Status updated')

def is_false_positive(video: SearchResult):
	if any(findall(r'newjeans|뉴진스|jeans', video.snippet.title, IGNORECASE)) & any(findall(r'react|hear|listen|watch', video.snippet.title, IGNORECASE)):
		log('Verified result')
		return False
	else:
		log('Identified false positive')
		return True

def is_duplicate(video: SearchResult):
	log('Checking for duplicate')
	db = load('videos.db', False)

	if video.id.videoId in db.getall():
		log('Found duplicate')
		return True
	else:
		log('No duplicate found')
		log('Adding video to database')
		db.set(video.id.videoId, True)
		db.dump()
		log('Video added to database')
		return False

def escape_formatting(text: str):
	return text.replace("&quot;", "\"").replace("&amp;", "&").replace("&#39;", "'")

def resolve_twitter_handle(channel_id: str, channel_name: str):
	try:
		# fetch config.json from github
		response = get('https://raw.githubusercontent.com/castdrian/nwjns-reactions/main/config.json')
		response.raise_for_status()

		# parse config.json
		config = response.json()
		for channel in config['channels']:
			if channel['id'] == channel_id:
				return channel['twitter_handle']
			
		return channel_name
	
	except Exception as e:
		log('Error: ' + str(e))
		return channel_name

def log(message: str):
	print(f'[{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}] {message}')