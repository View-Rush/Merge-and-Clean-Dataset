# Sri Lankan YouTube Video Analytics Dataset

## Overview
This dataset contains metadata of YouTube videos collected via the YouTube Data API v3. It is focused on Sri Lankan content but also contains global references.

## Data Source
- All data was collected via the official YouTube Data API v3.
- Only publicly available metadata is included (video ID, title, view counts, upload date, etc.).
- No video content or copyrighted media files are included.

## Usage Notes
- Users must comply with YouTube API Terms of Service: https://developers.google.com/youtube/terms/api-services-terms-of-service
- Redistribution of video content is prohibited.
- The dataset is versioned: each folder under `data/` corresponds to a dataset snapshot.

## Dataset Structure
- `data/` – CSV files with video metadata
- `logs/DAILY_LOG.md` – Daily collection log
- `data_dictionary.md` – Description of columns
- `changelog.md` – Dataset update history
- `metadata.json` – Machine-readable metadata

## License
This dataset is distributed under the YouTube API Terms of Service. See LICENSE for details.
