from libs.db import Database
import pika

from os import environ as env
import logging

# logging.basicConfig(level=(env.get("LOGGING_LEVEL", None) or logging.INFO))


def get_db():
	return Database(env['DATABASE_URL'])

def get_rmq():
	return pika.BlockingConnection(
		pika.ConnectionParameters('rabbitmq', 5672, '/', pika.PlainCredentials(env['RMQ_USERNAME'], env['RMQ_PASSWORD']))
	)

def get_logging_level():
	return env.get("LOGGING_LEVEL", None) or logging.INFO
def config_logging():
	logging.basicConfig(level=get_logging_level())

def setup_rmq():
	# Connect to RabbitMQ
	connection = get_rmq()
	channel = connection.channel()

	# Declare the queues
	channel.queue_declare(queue='channel_urls')
	channel.queue_declare(queue='parsed_videos')

	connection.close()

if __name__ == '__main__':
	config_logging()
	logging.info('Setting up RabbitMQ')
	setup_rmq()