export LOGGING_LEVEL=INFO;

cd src;
python3 declare.py &&  # Non blocking
python3 consumer.py & echo "Consumer PID "$! &&
python3 producer.py & echo "Producer PID "$!;

echo "--------------------------------"
echo "If required, kill consumer and/or producer using PIDs above"