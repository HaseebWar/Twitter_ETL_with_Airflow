from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import tweepy
import pandas as pd
import s3fs
import os

def run_twitter_etl():
    bearer_token = "YOUR_BEARER_TOKEN"  # <-- PUT your actual Bearer Token here

    # Authenticate to Twitter API
    client = tweepy.Client(bearer_token=bearer_token)

    # Get user ID of 'elonmusk'
    user = client.get_user(username='elonmusk')

    # Fetch tweets
    posts = client.get_users_tweets(
        id=user.data.id,
        max_results=100,  # API v2 max 100 tweets per request
        tweet_fields=['created_at', 'public_metrics'],
        exclude=['retweets']
    )

    tweet_list = []
    if posts.data:
        for post in posts.data:
            metrics = post.public_metrics
            refined_tweet = {
                "user": "elonmusk",
                "text": post.text,
                "favorite_count": metrics['like_count'],
                "retweet_count": metrics['retweet_count'],
                "created_at": post.created_at
            }
            tweet_list.append(refined_tweet)

    # Save DataFrame to S3
    df = pd.DataFrame(tweet_list)
    df.to_csv('s3://data-bucket/elonmusk_tweets.csv', index=False)

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 11, 8),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
dag = DAG(
    'twitter_dag',
    default_args=default_args,
    description='A simple Twitter ETL DAG that saves data to S3',
    schedule_interval=timedelta(hours=1),  # Runs every hour
    catchup=False,  # Don't backfill on start
)

# Define the task
run_etl = PythonOperator(
    task_id='complete_twitter_etl',
    python_callable=run_twitter_etl,
    dag=dag,
)

run_etl
