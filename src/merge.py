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

    # Initialize the merged dataframe with metadata
    merged_df = metadata_df.copy()

    # Add empty columns for daily statistics
    for col in daily_columns:
        merged_df[col] = np.nan

    print("Merging daily statistics...")

    # Process each video
    # Wrap the loop with tqdm for a progress bar
    for video_id in tqdm(merged_df['id'], desc="Merging videos", unit="video"):
        video_stats = stats_df[stats_df['videoId'] == video_id]

        if not video_stats.empty:
            # Group by dayIndex and fill the appropriate columns
            for _, row in video_stats.iterrows():
                day_index = row['dayIndex']

                if pd.notna(day_index) and 0 <= day_index <= 29:
                    day_index = int(day_index) + 1  # Convert to 1-based index

                    # Update the corresponding day columns
                    video_mask = merged_df['id'] == video_id

                    if pd.notna(row['viewCount']):
                        merged_df.loc[video_mask, f'day_{day_index}_views'] = row['viewCount']

                    if pd.notna(row['likeCount']):
                        merged_df.loc[video_mask, f'day_{day_index}_likes'] = row['likeCount']

                    if pd.notna(row['commentCount']):
                        merged_df.loc[video_mask, f'day_{day_index}_comments'] = row['commentCount']

    print(f"Merged data for {len(merged_df)} videos")
    print(merged_df.head())
    print(f"Total columns: {len(merged_df.columns)}")
    return merged_df


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
