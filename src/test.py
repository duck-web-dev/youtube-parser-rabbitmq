# Check RabbitMQconnection and setup queues   
from consumer import VideoConsumer
import declare



# Example usage
from producer import YoutubeParser
from main import get_db, get_rmq

from threading import Thread
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)

db = get_db()

parser = YoutubeParser(db, get_rmq, 3, '../bin')
consumer = VideoConsumer(db, get_rmq())

Thread(target=consumer.consume_videos).start()

print(f'Starting {len(parser.workers)} workers')
parser.start_workers()

# Parse channel URLs and send to RabbitMQ
# parser.parse_channel('@asdasd')
# parser.parse_channel('@123123')
# parser.parse_channel('@gitler_228_69_2012_1377_1488_993')
# parser.parse_channel('@mrbeast')
# parser.parse_channel('@matye_bal')


while True: 
	try:
		sleep(1000)
	except KeyboardInterrupt:
		print('Aborting... Please wait for workers to finish processing last message.')
		parser.stop_workers()
		exit()