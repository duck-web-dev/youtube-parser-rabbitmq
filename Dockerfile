FROM ubuntu:latest

# Basic requirements: python, postgres, utils
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
	libpq-dev  \
    postgresql-client \
	curl wget jq unzip	
	
# libdbus-1-3 libdbus-1-dev libglib2.0-dev libcairo2-dev pkg-config
# DEV
RUN apt-get install -y iputils-ping;

# RabbitMQ
ENV RABBITMQ_MANAGEMENT_ALLOW_WEB_ACCESS="true"
ENV ELIXIR_ERL_OPTIONS="+fnu"

# Common knowlege: This step should happen as late as possible
WORKDIR /app
COPY . .

# Pip packages
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Chrome and chromedriver (required for parser)
RUN bash ./scripts/get_recent_chrome.sh $(realpath ./bin)


CMD ./scripts/run.sh;
