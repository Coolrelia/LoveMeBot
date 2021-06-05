from TwitterAPI import TwitterAPI
import datetime

import os
import sys

VIDEO_FILENAME = 'LoveMe.mp4'
TWEET_TEXT = 'mood'

api = TwitterAPI("kj3w4Qa9gACY96ydqdr4WMiPi", "lAVfU9rPewKA2Z24LbXVuDoss9qZC8uzfEnysLqqszyWucvrv9",
				 "1366597445073973251-cXkBpK829ImdxyzHH03L5BrcyWJIAO", "WXjoGKX5LPFT6HXfqNKzPDdYN7jTharEi2yRKU9iC83zp")

if datetime.date.today().weekday() == 4:
	bytes_sent = 0
	total_bytes = os.path.getsize(VIDEO_FILENAME)
	file = open(VIDEO_FILENAME, 'rb')


	def check_status(r):
		# EXIT PROGRAM WITH ERROR MESSAGE
		if r.status_code < 200 or r.status_code > 299:
			print(r.status_code)
			print(r.text)
			sys.exit(0)


	r = api.request('media/upload', {'command': 'INIT', 'media_type': 'video/mp4', 'total_bytes': total_bytes})
	check_status(r)

	media_id = r.json()['media_id']
	segment_id = 0

	while bytes_sent < total_bytes:
		chunk = file.read(4 * 1024 * 1024)
		r = api.request('media/upload', {'command': 'APPEND', 'media_id': media_id, 'segment_index': segment_id},
						{'media': chunk})
		check_status(r)
		segment_id = segment_id + 1
		bytes_sent = file.tell()
		print('[' + str(total_bytes) + ']', str(bytes_sent))

	r = api.request('media/upload', {'command': 'FINALIZE', 'media_id': media_id})
	check_status(r)

	r = api.request('statuses/update', {'status': TWEET_TEXT, 'media_ids': media_id})
	check_status(r)