import logging
from libs.db import Database
import pika
import json


class VideoConsumer:
	def __init__(self, db: Database, rabbitmq: pika.BlockingConnection):
		self.logger = logging.getLogger("VideoConsumer")
		self.db = db
		self.rmq = rabbitmq

	def consume_videos(self):
		''' Call to activate consumer and start consuming messages. \n\n !Warning: `blocking method`. '''
		
		self.logger.info('Started consuming videos')
		channel = self.rmq.channel()
		# channel.basic_qos(prefetch_count=50, global_qos=False)

		def callback(ch, method, properties, body):
			ack_id = method.delivery_tag
			try:
				self.save_to_database(body.decode())
				channel.basic_ack(ack_id)
			except:
				channel.basic_nack(ack_id)


		channel.basic_consume(queue='parsed_videos', on_message_callback=callback, auto_ack=False)
		channel.start_consuming()

	def save_to_database(self, parsed_data: str):
		''' Save consumed parsed video data to database. '''
		self.logger.debug('Consumer got parsed data:', parsed_data)
		try:
			data = json.loads(parsed_data)
		except Exception as e:
			self.logger.error('Failed to decode json from parsed data (what?)', exc_info=True)
		try:
			self.db.create_video(*data[:3])
		except:
			self.logger.error('Failed to save this data to db:', data, exc_info=True)
		

if __name__ == '__main__':
	from declare import get_db, get_rmq, config_logging
	config_logging()
	VideoConsumer(get_db(), get_rmq()).consume_videos()