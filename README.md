# Rinha de Backend 2025 - My Submission

![Galinha da Rinha :)](https://raw.githubusercontent.com/zanfranceschi/rinha-de-backend-2025/refs/heads/main/misc/imgs/header.jpg)

Rinha de Backend is an yearly challenge pitting up backend developers to compete for glory.
Each edition brings a new theme, and the 2025th edition tackled Payment Processing. Developers
were tasked with creating an API for intermediating requests to two different Payment Processors.

This edition of the Rinha de Backend had two key metrics: total profit and 99th percentile
response time. My results when attempting the challenge can be found on ```partial-results.json```.

### Install

The application is fully containerized and can be run using Docker. An image is also available on
[DockerHub](https://hub.docker.com/repository/docker/victorcoelh/rinha-backend-2025-app/general).
Running this application requires an existing installation of Docker.

To run the official testing suite for the first stage of the Rinha de Backend 2025, you'll also
need to install [k6](https://github.com/grafana/k6?tab=readme-ov-file).

### Usage

You'll need an instace of both Payment Processor containers running to execute the project. A compose
file for running both Payment Processors is available in rinha/payment-processor for convenience.

```docker compose -f rinha/payment-processor/docker-compose.yml up -d```

Then, you'll need to build and run this application using Docker:

```
docker compose build
docker compose up -d
```

The server will then be available on http://localhost:9999.

You can also run the existing tests for the Rinha de Backend 2025, available in rinha/rinha-test with
k6, by running the following command:

```k6 run rinha/rinha-test/rinha.js```
