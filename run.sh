export LOGGING_LEVEL=INFO;

cd src;

# Setup RabbitMQ
python3 declare.py &&

# Run consumers in screen sessions
tmux new-session -d -s "db_consumer"		"python3 db_consumer.py" &
tmux new-session -d -s "parser_consumer"	"PARSER_WORKERS="$PARSER_WORKERS" python3 parser_consumer.py" &;

# For docker not to shut down
for ((;;)) do sleep infinity; done;