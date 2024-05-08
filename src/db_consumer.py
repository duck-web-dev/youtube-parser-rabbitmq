import logging
import json
import pika
from libs.db import Database


class DbConsumer:
	def __init__(self, db: Database, rabbitmq: pika.BlockingConnection):
		self.logger = logging.getLogger("DbConsumer")
		self.db = db
		self.rabbitmq = rabbitmq

	def consume_videos(self):
		'''Call to start consuming parsed videos and saving them to database.
		
		!Warning: blocking method.'''
		
		self.logger.info('Started consuming videos')
		channel = self.rabbitmq.channel()

		def callback(ch, method, properties, body):
			ack_id = method.delivery_tag
			try:
				self.save_video_to_database(body.decode())
				channel.basic_ack(ack_id)
			except:
				channel.basic_nack(ack_id)

		channel.basic_consume(queue='parsed_videos', on_message_callback=callback, auto_ack=False)
		channel.start_consuming()

	def save_video_to_database(self, parsed_data: str):
		''' Save special parsed data from queue `parsed_videos` to database. 
		
		If you just need to save to database, use `Database.create_video` from libs.db.'''
		
		try:
			data = json.loads(parsed_data)
		except Exception as e:
			self.logger.error('Failed to decode json from parsed data', exc_info=True)
			return

		try:
			video_id, username, href, *_ = data
		except Exception as e:
			self.logger.error('Invalid data recieved', exc_info=True)
			return

		self.logger.info(f'Saving video to db: {video_id}')
		try:
			self.db.create_video(video_id, username, href)
		except Exception as e:
			self.logger.error(f'Failed to save video data to db: {data}', exc_info=True)


if __name__ == '__main__':
	# If ran as a script, start consuming and processing
	
	from declare import get_db, get_rmq, config_logging

	config_logging()

	consumer = DbConsumer(get_db(), get_rmq())
	consumer.consume_videos()
