from libs.parser import YTParserWorker
from libs.db import Database
from typing import Callable
import os, os.path as path
import time
import logging
import pika


class YoutubeParser:
	def __init__(self, db: Database, rmq_factory: Callable[[], pika.BlockingConnection], num_workers: int, bin_path: str):
		if num_workers < 1:
			raise ValueError('At least one worker is required')
		self.num_workers = num_workers

		self.db = db
		self.channel = rmq_factory().channel()
		self._ready = False

		# Create workers
		chrome_bin_path			= path.join(bin_path, 'chrome-linux64', 'chrome')
		chromedriver_bin_path	= path.join(bin_path, 'chromedriver-linux64', 'chromedriver')
		self.workers: list[YTParserWorker] = []
		for i in range(self.num_workers):
			worker = YTParserWorker(lambda: rmq_factory().channel(), i)  # chrome_bin_path, chromedriver_bin_path
			self.workers.append(worker)
	
	def __del__(self):
		self.channel.close()

	def start_workers(self):
		# Start worker processes
		for worker in self.workers:
			worker.start()
		self._ready = True
	
	def stop_workers(self):
		for worker in self.workers:
			worker.stop_consuming()
		self._ready = False

	def parse_channel(self, channel_url: str):
		if not self._ready:
			raise RuntimeError('Workers are not ready, use `start_workers` method.')
		if 'http' not in channel_url:
			channel_url = 'https://' + channel_url 		# Basic case if user forgot scheme, safe because later url is verified again
		self.channel.basic_publish(exchange='', routing_key='channel_urls', body=channel_url)