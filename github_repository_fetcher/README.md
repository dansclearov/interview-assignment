# GitHub Repository Fetcher

A scalable Django application for fetching and storing top GitHub repositories with their associated tags.

## Overview

This application allows you to fetch any number of top GitHub repositories (sorted by stars) along with their tags. It uses GitHub's GraphQL API for efficient data retrieval and implements a background processing system to handle large requests without blocking the web server.

## Features

- **Asynchronous Processing**: Uses Celery for background task processing
- **Efficient API Usage**: Leverages GitHub's GraphQL API to minimize request count
- **Rate Limit Awareness**: Implements backoff strategies to respect GitHub API limits
- **Progress Tracking**: Provides job status endpoints to monitor progress
- **Scalable Design**: Capable of handling requests for millions of repositories over time

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install and start Redis (for Celery):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server
   # macOS
   brew install redis && brew services start redis
   ```

3. Set up your environment:
   ```bash
   # Create a .env file
   echo "GITHUB_TOKEN=your_github_personal_access_token" > .env
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

## Usage

1. Start the Django server:
   ```bash
   python manage.py runserver
   ```

2. Start the Celery worker:
   ```bash
   celery -A github_repo_fetcher worker -l INFO
   ```

3. Use the provided Postman collection to interact with the API endpoints:
   - Fetch repositories
   - Check job status
   - View repositories

## API Endpoints

- **POST /api/repositories/fetch**: Start a repository fetch job
- **GET /api/jobs/{job_id}/status**: Check the status of a fetch job
- **GET /api/repositories**: List fetched repositories (paginated)
- **GET /api/repositories/{repo_id}**: Get details of a specific repository

## Design Considerations

- **Rate Limiting**: GitHub's API limits (5,000 points/hour) are the primary bottleneck, not processing speed
- **Database Schema**: Optimized for efficient querying of repository data
- **Error Handling**: Robust error capture and reporting through job status
- **Scalability**: The system can handle requests for any number of repositories by processing them over time

## Limitations

- Processing large numbers of repositories (e.g., 1M+) will take significant time due to GitHub API rate limits
- The system is designed to fetch repositories sequentially to avoid rate limit issues
