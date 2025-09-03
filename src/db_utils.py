"""
Utility functions for connecting to Aiven PostgreSQL and BigQuery.
"""
import os
import psycopg2
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_postgres_connection():
    """Create and return a PostgreSQL connection."""
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        database=os.getenv('POSTGRES_DB')
    )

def get_bigquery_client():
    """Create and return a BigQuery client."""
    credentials_path = os.getenv('BIGQUERY_CREDENTIALS_PATH')
    if credentials_path:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    
    project_id = os.getenv('BIGQUERY_PROJECT_ID')
    return bigquery.Client(project=project_id)

def fetch_video_metadata():
    """Fetch video metadata from Aiven PostgreSQL."""
    conn = get_postgres_connection()
    
    query = """
    SELECT 
        id,
        published_at,
        channel_id,
        title,
        description,
        localized_title,
        localized_description,
        thumbnail_default,
        thumbnail_medium,
        thumbnail_high,
        tags,
        category_id,
        live_broadcast_content,
        default_language,
        default_audio_language,
        video_duration,
        view_count,
        likes_count,
        favourite_count,
        comment_count,
        inserted_at
    FROM public.videos
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def fetch_video_stats():
    """Fetch video statistics from BigQuery."""
    client = get_bigquery_client()
    dataset = os.getenv('BIGQUERY_DATASET')
    table = os.getenv('BIGQUERY_TABLE')
    
    query = f"""
    SELECT 
        videoId,
        recordedAt,
        dayIndex,
        viewCount,
        likeCount,
        commentCount,
        fetchedFrom
    FROM `{client.project}.{dataset}.{table}`
    ORDER BY videoId, dayIndex
    """
    
    df = client.query(query).to_dataframe()
    return df
