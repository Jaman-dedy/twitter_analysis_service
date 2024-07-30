# Twitter Analysis Service

## Overview
This project is a web service for analyzing Twitter data. It provides APIs for user recommendations and other Twitter-related analytics.

## Table of Contents
- [Twitter Analysis Service](#twitter-analysis-service)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Project Structure](#project-structure)
  - [Setup](#setup)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
  - [API Endpoints](#api-endpoints)
  - [Development](#development)
  - [Troubleshooting](#troubleshooting)

## Prerequisites
- Docker and Docker Compose
- Python 3.9+
- PostgreSQL

## Project Structure
twitter_analysis_service/
├── app/
│   ├── api/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── init.py
│   ├── config.py
│   └── main.py
├── etl/
│   ├── init.py
│   ├── etl_process.py
│   └── run_etl.py
├── tests/
│   ├── init.py
│   └── conftest.py
├── .env
├── .gitignore
├── create_test_db.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run_tests.sh
└── README.md

## Setup

1. Clone the repository:

git clone https://github.com/your-username/twitter_analysis_service.git
cd twitter_analysis_service

2. Create a `.env` file in the project root and add the following:

POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=twitter_analysis

3. Build the Docker images:

docker-compose build

## Running the Application

1. Start the services:

docker-compose up

2. The API will be available at `http://localhost:8000`.

3. To stop the services:

docker-compose down

## Running Tests

1. Ensure the database service is running:

./run_tests.sh

This script will:
- Set up a virtual environment
- Install dependencies
- Run pytest

## API Endpoints

- `GET /`: Welcome message
- `GET /api/recommendations/q2`: User recommendations
- Query Parameters:
 - `user_id`: string
 - `type`: string (reply, retweet, or both)
 - `phrase`: string (percent-encoded)
 - `hashtag`: string

For detailed API documentation, visit `http://localhost:8000/docs` when the application is running.

## Development

1. Create a virtual environment:


## Troubleshooting

- If you encounter database connection issues, ensure the PostgreSQL service is running and the connection details in `.env` are correct.
- For import errors when running tests, make sure you're using the virtual environment and the `PYTHONPATH` is set correctly.
- If changes are not reflected, try rebuilding the Docker images:

