import sys
import pika
from declare import get_rmq


# Check argv
if len(sys.argv) != 2:
	print("Usage: python main.py <urls_list.txt>")
	sys.exit(1)

# Read from file
urls_file = sys.argv[1]
try:
	with open(urls_file, 'r') as f:
		urls = f.readlines()
except FileNotFoundError:
	print(f"Error: File '{urls_file}' not found.")
	sys.exit(1)

# Open RabbitMQ channel
rmq = get_rmq()
channel = rmq.channel()

# Publick urls to queue
for url in urls:
	print(f'Publishing url "{url}" ...')
	channel.basic_publish(exchange='', routing_key='channel_urls', body=url.strip())
	print('Ok')

channel.close()
rmq.close()

print('All urls published')