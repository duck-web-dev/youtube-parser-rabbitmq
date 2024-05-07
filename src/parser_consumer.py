from typing import Callable
from os import path
import logging

from libs.parser.main import YTParserWorker
import pika


class VideosConsumer:
	def __init__(self, rmq_factory: Callable[[], pika.BlockingConnection], num_workers: int, bin_path: str):
		if num_workers < 1:
			raise ValueError('At least one worker is required')
		self.num_workers = num_workers
		self.logger = logging.getLogger("VideosConsumer")

		# Create workers
		chrome_bin_path			= path.join(bin_path, 'chrome-linux64', 'chrome')
		chromedriver_bin_path	= path.join(bin_path, 'chromedriver-linux64', 'chromedriver')

		self.workers: list[YTParserWorker] = []
		for worker_uniquie_id in range(self.num_workers):
			worker = YTParserWorker(
				lambda: rmq_factory().channel(),
				worker_uniquie_id,
				chrome_bin_path, chromedriver_bin_path
			)
			self.workers.append(worker)
	
	def __del__(self):
		for worker in self.workers:
			worker.stop_consuming()

	def start_workers(self):
		''' Start workers and start consuming, blocking method. 
		
		This method can only be called once, workers cannot be restarted.
		'''
		
		self.logger.info(f'Starting {len(self.workers)} workers')
		if self.num_workers != len(self.workers):
			self.logger.warning('IMPORTANT! `num_workers` and actual number of workers is different. This should not happen!')

		for worker in self.workers:
			worker.start()
		
		for worker in self.workers:
			worker.join()


if __name__ == '__main__':
	# If ran as a script, start consuming and processing
	from declare import get_rmq, config_logging, env
	
	config_logging()

	num_workers: int = env.get('PARSER_WORKERS', None)
	if num_workers is None:
		logging.warning('Number of workers not set, using default. Use `PARSER_WORKERS` env variable to change this.')
		num_workers = 3

	consumer = VideosConsumer(get_rmq, num_workers, '../bin')
	consumer.start_workers()