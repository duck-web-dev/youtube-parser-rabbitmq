# 20.04 runs chrome with less adidtional
FROM ubuntu:22.04

# For apt-get not to prompt anything when configuring packages
ENV DEBIAN_FRONTEND noninteractive

# Basic requirements: python, postgres, utils
RUN apt-get update
RUN apt-get install -y \
	python3-pip python3-dev \
	libpq-dev  \
    postgresql-client \
	software-properties-common curl wget jq unzip iputils-ping tmux

# Libs for chrome and chromedriver
RUN add-apt-repository -y universe && apt update;
RUN apt-get install -y xvfb libxi6 libgconf-2-4 libjq1 libonig5 libxkbcommon0 libxss1 libglib2.0-0 libnss3 \
  libfontconfig1 libatk-bridge2.0-0 libatspi2.0-0 libgtk-3-0 libpango-1.0-0 libgdk-pixbuf2.0-0 libxcomposite1 \
  libxcursor1 libxdamage1 libxtst6 libappindicator3-1 libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libxfixes3 \
  libdbus-1-3 libexpat1 libgcc1 libnspr4 libgbm1 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxext6 \
  libxrandr2 libxrender1 gconf-service ca-certificates fonts-liberation libappindicator1 lsb-release xdg-utils

# libdbus-1-3 libdbus-1-dev libglib2.0-dev libcairo2-dev pkg-config

# RabbitMQ
ENV RABBITMQ_MANAGEMENT_ALLOW_WEB_ACCESS="true"
ENV ELIXIR_ERL_OPTIONS="+fnu"

# Common knowlege: This step should happen as late as possible
WORKDIR /app
COPY . .

# Pip packages
RUN pip3 install --no-cache-dir -r requirements.txt  # Since Python3.11  --break-system-packages

# Chrome and chromedriver (required for parser)
RUN bash ./scripts/get_recent_chrome.sh $(realpath ./bin)


CMD bash ./run.sh;
