# Twitter_ETL_with_Airflow

A simple Apache Airflow 3.0 DAG to extract tweets from Elon Musk's Twitter account, process the data, and load it into an Amazon S3 bucket.

## Project Overview

- **Extract:** Fetches latest tweets using Twitter API v2 and Tweepy.
- **Transform:** Processes important tweet fields like text, favorite count, retweet count, and timestamps.
- **Load:** Saves the structured data as a CSV file directly into an Amazon S3 bucket.

## Technologies Used

- Apache Airflow 3.0
- Python 3.10
- Tweepy
- Pandas
- S3FS

## DAG Details

- **DAG ID:** `twitter_dag`
- **Schedule:** Every 1 hour (`schedule=timedelta(hours=1)`)
- **Operator:** `PythonOperator`
- **Output:** CSV saved at `s3://(bucket_name)/elonmusk_tweets.csv`
- **Best Practices Followed:**
  - Minimal top-level code
  - Uses `with DAG(...)` context manager
  - Compatible with Airflow 3.0+

## Setup Instructions

1. Install required Python packages:
    ```bash
    pip install apache-airflow tweepy pandas s3fs
    ```

2. Initialize and start Airflow:
    ```bash
    airflow db init
    airflow standalone
    ```

3. Place `twitter_dag.py` inside your Airflow `dags/` directory.

4. Access the Airflow web UI at `http://localhost:8080`, find `twitter_dag`, and trigger manually or wait for the scheduled run.

## Folder Structure
airflow/ └── dags/ └── twitter_dag.py


## Important Notes

- Update the S3 bucket name if needed.
- Keep your Twitter API Bearer Token secure.
- Ensure AWS credentials are properly configured for S3 access.
- **Free Twitter API Limitations:**
  - With the free tier of the Twitter API, you can only extract up to **100 posts** in a single request.
  - There is also a **rate limit** that restricts how frequently you can make requests to the API, so be mindful of this when scheduling the DAG.
  - If you need more data or higher request limits, consider upgrading to a paid API tier.

# 🚀 Ready to Extract, Transform, and Load Twitter Data!

