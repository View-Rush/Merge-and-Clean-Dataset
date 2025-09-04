"""
Script to merge data from Aiven PostgreSQL and BigQuery into a CSV file.
Combines video metadata from PostgreSQL with 30-day statistics from BigQuery.
"""
import pandas as pd
import numpy as np
from datetime import datetime
from db_utils import fetch_video_metadata, fetch_video_stats
import yaml
import os
from tqdm import tqdm

def load_config():
    """Load configuration from config.yaml."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def create_daily_columns():
    """Create column names for 30 days of statistics."""
    columns = []
    for day in range(1, 31):  # Days 1-30
        columns.extend([
            f'day_{day}_views',
            f'day_{day}_likes', 
            f'day_{day}_comments'
        ])
    return columns

def merge_video_data():
    """
    Merge video metadata from PostgreSQL with daily statistics from BigQuery.
    Creates 90 additional columns (30 days × 3 metrics).
    """
    print("Fetching video metadata from Aiven PostgreSQL...")
    metadata_df = fetch_video_metadata()
    print(f"Fetched {len(metadata_df)} videos from PostgreSQL")
    print(metadata_df.head())
    
    print("Fetching video statistics from BigQuery...")
    stats_df = fetch_video_stats()
    print(f"Fetched {len(stats_df)} statistics records from BigQuery")

    # Create columns for 30 days of data
    daily_columns = create_daily_columns()

    # Add empty columns for daily statistics
    # Pivot stats_df to wide format: one row per videoId, columns for each day's metrics
    stats_pivot = stats_df.copy()

    # Ensure dayIndex is integer and 1-based
    stats_pivot = stats_pivot[stats_pivot['dayIndex'].notna()]
    stats_pivot['dayIndex'] = stats_pivot['dayIndex'].astype(int) + 1

    # Pivot to get columns like day_1_views, day_1_likes, etc.
    stats_wide = stats_pivot.pivot_table(
        index='videoId',
        columns='dayIndex',
        values=['viewCount', 'likeCount', 'commentCount'],
        aggfunc='first'
    )

    # Flatten MultiIndex columns and rename
    stats_wide.columns = [
        f'day_{day}_{metric.replace("Count", "").lower() + "s"}'
        for metric, day in stats_wide.columns
    ]
    stats_wide = stats_wide.reset_index()

    # Merge with metadata_df
    merged_df = metadata_df.merge(stats_wide, left_on='id', right_on='videoId', how='left')

    # Drop the redundant videoId column from stats_wide
    merged_df = merged_df.drop(columns=['videoId'])

    # Ensure all daily columns are present (fill missing ones with NaN)
    for col in daily_columns:
        if col not in merged_df.columns:
            merged_df[col] = pd.NA
        merged_df[col] = merged_df[col].astype("Int64")

    # Reorder columns
    merged_df = reorder_columns(merged_df)

    print(f"Merged data for {len(merged_df)} videos")
    print(merged_df.head())
    print(f"Total columns: {len(merged_df.columns)}")
    return merged_df

def reorder_columns(merged_df):
    """Reorder columns so that all views, then likes, then comments are grouped."""
    # Keep non-daily columns first
    non_daily = [col for col in merged_df.columns if not col.startswith("day_")]

    # Collect ordered daily columns
    views = [f"day_{i}_views" for i in range(1, 31)]
    likes = [f"day_{i}_likes" for i in range(1, 31)]
    comments = [f"day_{i}_comments" for i in range(1, 31)]

    ordered_columns = non_daily + views + likes + comments
    return merged_df[ordered_columns]

def save_to_csv(df, output_path):
    """Save the merged dataframe to CSV."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'merged_data_{timestamp}.csv'

    # Update output path with timestamp
    output_dir = os.path.dirname(output_path)
    timestamped_path = os.path.join(output_dir, filename)

    # Save to CSV
    df.to_csv(timestamped_path, index=False)
    print(f"Merged data saved to: {timestamped_path}")

    # Print summary statistics
    print(f"\nSummary:")
    print(f"Total videos: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Daily statistics columns: {len([col for col in df.columns if col.startswith('day_')])}")

def main():
    """Main function to execute the merge process."""
    try:
        print("Starting video data merge process...")
        
        # Load configuration
        config = load_config()
        output_path = config.get('output', {}).get('csv_path', '../data/merged_output.csv')
        print(f"Output path: {output_path}")
        
        # Convert relative path to absolute
        if output_path.startswith('../'):
            output_path = os.path.join(os.path.dirname(__file__), output_path)
        
        # Merge the data
        merged_df = merge_video_data()
        
        # Save to CSV
        save_to_csv(merged_df, output_path)
        
        print("\nMerge process completed successfully!")
        
    except Exception as e:
        print(f"Error during merge process: {str(e)}")
        raise

if __name__ == "__main__":
    main()
