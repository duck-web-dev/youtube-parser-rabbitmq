**Simple YouTube Channel Parser**

This project is a simple YouTube channel parser that extracts all videos available on the front page of specified channels and saves them to a PostgreSQL database. It utilizes Python, Selenium with Chrome, RabbitMQ, and Docker Compose for its stack.

### Setup

1. Clone/download the repo
2. Create a `.env` file based on `.env.example` with actual values for environment variables. Pls make sure not to publish the actual ".env" to github, its added to gitignore.
4. Build and start docker container.
    ```bash
    docker compose up -d --build
    ```

### Usage

1. Enter the container shell (default name is `yt-parse-container`, but double check it via `docker ps`):
    ```bash
    docker compose exec yt-parse-container bash
    ```
2. To start processing your channels, run the `main.py` script with the list of channel URLs. e.g.:
    ```bash
    python src/main.py data/example.txt
    ```

3. You can also:
- Aces the RabbitMQ management interface at `localhost:15672` (port is forwarded to your host machine) with the user/pass from `.env`.
- Increase of decrease number of parser workers (default is 3) by uncommenting the `PARSER_WORKERS` variable in `.env`. Each worker runs an instance of chrome and chromium, so they are pretty resource intensive.

### Tips:
If you need to connect to PostgreSQL on the host machine:
1. Set `listen_addresses` in postgres config. 
2. Either:
- Use your host IP from `docker0` network (can be found at `ip route` )
- Assign a static IP to your host, and use it. (This method works better)