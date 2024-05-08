export LOGGING_LEVEL=INFO;

cd src;

# Setup RabbitMQ
python3 declare.py &&

# Run consumers in screen sessions
screen -S db_consumer		-d -m "python3 db_consumer.py" &
screen -S parser_consumer	-d -m "PARSER_WORKERS="$PARSER_WORKERS" python3 parser_consumer.py" &;

# For docker not to shut down
for ((;;)) do sleep infinity; done;