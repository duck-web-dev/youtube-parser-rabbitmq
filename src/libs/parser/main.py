from multiprocessing import Process
from typing import Callable
from pika.adapters.blocking_connection import BlockingChannel

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

import pika
import re
import time
import json
import logging




class YTParserWorker(Process):
	def __init__(self, channel_factory: Callable[[], BlockingChannel], worker_id: int):
		'''
		Initialize a Worker instance.

		Args:
			channel_factory (() -> BlockingChannel): Function that creates unique BlockingChannel (as pika is not thread safe).
			worker_id (int): Any unique number to identify worker, used in logs.
		'''
		self.logger = logging.getLogger("YTParserWorker")
		super().__init__()
		self.channel = channel_factory()
		self.channel.basic_qos(prefetch_count=3, global_qos=False)
		self._id = worker_id
		self.logger.info(f'Worker {self._id} created')

	def run(self):
		try:
			self.channel.basic_consume(queue='channel_urls', on_message_callback=self.parse_and_publish)
			self.channel.start_consuming()
		except KeyboardInterrupt:
			self.stop_consuming()

	def parse_and_publish(self, ch, method, properties, body):
		ack_id = method.delivery_tag
		channel_url = body.decode()
		self.logger.info(f'Worker {self._id} got url {channel_url} (tag {ack_id})')
		try:
			parsed_data = self.parse_channel(channel_url)
			self.channel.basic_publish(exchange='', routing_key='parsed_videos', body=parsed_data)
			self.channel.basic_ack(ack_id)
		except:
			self.channel.basic_nack(ack_id)

	def parse_channel(self, channel_url: str):
		time.sleep(5)
		return json.dumps((channel_url.split('@')[-1][:11], channel_url, 1))

	def stop_consuming(self):
		self.channel.stop_consuming()

	def __del__(self):
		self.logger.info(f'Worker {self._id} destroyed')

# class YTParserWorker:
# 	def __init__(self, chrome_bin_path, chromedriver_bin_path):
# 		self._lock = False  # Indicates if a worker is busy or not
		
# 		options = webdriver.ChromeOptions()
# 		options.binary_location = chrome_bin_path
# 		options.page_load_strategy = 'eager'

# 		self.driver = webdriver.Chrome(
# 			options = options,
# 			service = webdriver.ChromeService(
# 				chromedriver_bin_path
# 			)
# 		)


# 	def __del__(self):
# 		self.logger.info("Worker destroyed, killing selenium browser")
# 		self.driver.quit()


# 	def parse_channel(self, channel_url: str) -> tuple[str, list[str]]:
# 		'''
# 		Parse the YouTube channel.

# 		Args:
# 			channel_link (str): The link to the YouTube channel. E.g. `https://youtube.com/@username`.

# 		Returns:
#         	tuple[str, list[str]]: A tuple containing channel usernamne and list of `video_id` strings
# 		'''

# 		# Run checks
# 		if self._lock:
# 			raise RuntimeError("Worker is busy. Can only parse one channel at a time.")
# 		self._lock = True

# 		ir_url_valid	= re.match(r'^https?://(?:www\.)?youtube\.com/@\w+$',			channel_url)

# 		if not ir_url_valid:
# 			if 'http' not in channel_url:
# 				raise ValueError("Invalid channel url: no scheme")
# 			else:
# 				raise ValueError("Invalid channel url: see docstring for examples")
# 		else:
# 			channel = channel_url.split('/')[-1][1:]

# 		# Download page
# 		self.logger.info(f"Parser start for channel '@{channel}'")
# 		self.driver.get(channel_url)
		
# 		# Prepare to parse
# 		videos_wrapper_selector	= "#scroll-outer-container > #scroll-container > #items"
# 		video_el_selector		= f"{videos_wrapper_selector} > ytd-grid-video-renderer"
# 		data = set()
# 		def process_video_elements(items: list[WebElement]):
# 			for video_el in items:
# 				try:
# 					thumbnail_anchor_el = video_el.find_element(By.CSS_SELECTOR, "div#dismissible > ytd-thumbnail > a")
# 					href = thumbnail_anchor_el.get_attribute("href")
# 				except:
# 					logging.error('Couldn\'t process a video: couldn\'t find href. IF YOU SEE THIS ERROR, css selectors in parser need to be updated.')
# 				video_id = href.split('?v=')[1]
# 				logging.debug(f'Saving video {video_id} from channel @{channel}')
# 				data.add(video_id)

# 		# Parsing logic (actual parsing happens here)
# 		try:
# 			el: WebElement = WebDriverWait(self.driver, 60).until(
# 				EC.presence_of_element_located((By.CSS_SELECTOR, videos_wrapper_selector)) #This is a dummy element
# 			)
# 			# time.sleep(1)  # Give time for all video elements to be loaded by JS and rendered
			
# 			new_vids_available = True  # Repeat parsing untill it's possible to press next button and load more items
# 			while new_vids_available:
# 				process_video_elements(
# 					self.driver.find_elements(By.CSS_SELECTOR, video_el_selector)
# 				)
# 				try:
# 					x = self.driver.find_element(
# 						By.CSS_SELECTOR, "#right-arrow yt-button-shape > button > .yt-spec-button-shape-next__icon"
# 					)
# 					if x.is_displayed():
# 						# x.click()  # Doesn't work: "Other element would receive the click", and no way to disable this warning
# 						logging.debug('Loading more vids...')
# 						self.driver.execute_script("arguments[0].click();", x)
# 						time.sleep(0.5)
# 					else:
# 						new_vids_available = False
# 				except Exception as e:
# 					new_vids_available = False
# 			logging.debug(f'All ({len(data)}) videos parsed from channel @{channel}')
# 		except Exception as e:
# 			# raise RuntimeError("No videos were found", e)
# 			self.logger.warning("No videos were found on page (could be channel without videos, nonexistent channel or parsing error). Trace:", exc_info=True)
# 		finally:
# 			self.logger.info("Parser done, closing tab")
# 			# self.driver.close()
		
# 		self._lock = False

# 		return channel, list(data)