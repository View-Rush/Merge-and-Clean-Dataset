## Data Dictionary for Sri Lankan YouTube Video Analytics Dataset

### Dataset Overview
| Field                 | Description                                                                                                                                             |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Dataset Name**      | Sri Lankan YouTube Video Analytics Dataset                                                                                                              |
| **Dataset Size**      | \~50–60 MB per daily snapshot (grows daily; see changelog for exact size)                                                                               |
| **Date of Release**   | 2025-09-15 (first release); daily snapshots versioned thereafter                                                                                        |
| **No. of Attributes** | 111 columns (see Data Dictionary for details)                                                                                                           |
| **No. of Records**    | \~10k–20k videos (see changelog for exact counts)                                                                                                       |
| **Data Source**       | YouTube Data API v3                                                                                                                                     |
| **Data Privacy**      | Publicly available metadata only; no personally identifiable information                                                                                |
| **Notes**             | Each snapshot represents the state of YouTube videos as of collection date.                                                                             |
| **Prepared By**       | Group 21 - Data Science Project - CSE UoM                                                                                                               |
| **Point of Contact**  | [kevin.22@cse.mrt.ac.lk](kevin.22@cse.mrt.ac.lk)                                                                                                        |
| **Team Members**      | [Kevin Sanjula](https://github.com/Ke-vin-S)<br/>[ Pasindu Senevirathne ](https://github.com/L0rd008)<br/>[Shaamma Sajahan](https://github.com/Shaamma) |

### Attribute Overview
| Column Name                          | Type        | Description / Notes                                                                      |
|--------------------------------------|-------------|------------------------------------------------------------------------------------------|
| `id`                                 | string      | YouTube video ID (unique identifier).                                                    |
| `published_at`                       | datetime    | Date and time the video was published(UTC).                                              |
| `channel_id`                         | string      | Unique ID of the channel that published the video.                                       |
| `title`                              | string      | Title of the video.                                                                      |
| `description`                        | string      | Full description of the video.                                                           |
| `localized_title`                    | string      | Localized version of the title (if available).                                           |
| `localized_description`              | string      | Localized description of the video (if available).                                       |
| `thumbnail_default`                  | string      | URL of the default thumbnail image.                                                      |
| `thumbnail_medium`                   | string      | URL of medium-resolution thumbnail image.                                                |
| `thumbnail_high`                     | string      | URL of high-resolution thumbnail image.                                                  |
| `tags`                               | list/string | List of tags associated with the video. (stored as a stringified Python list)            |
| `category_id`                        | int         | YouTube category ID of the video.                                                        |
| `live_broadcast_content`             | string      | Indicates if video is live, none, or upcoming.                                           |
| `default_language`                   | string      | Default language code of the video (ISO 639-1).                                          |
| `default_audio_language`             | string      | Default audio language code of the video (ISO 639-1).                                    |
| `video_duration`                     | string      | Duration of the video in ISO 8601 format (e.g., PT1M5S = 1 minute 5 seconds).            |
| `view_count`                         | int/float   | Total number of views as of `inserted_at`.                                               |
| `likes_count`                        | float       | Total number of likes.                                                                   |
| `favourite_count`                    | int/float   | Total number of favourites (historically used; often 0).                                 |
| `comment_count`                      | float       | Total number of comments.                                                                |
| `inserted_at`                        | datetime    | Timestamp when this row was inserted into metadata database(UTC).                        |
| `day_1_views` … `day_30_views`       | int         | Cumulative view counts for each day after publication (day 1 = first day after publish). |
| `day_1_likes` … `day_30_likes`       | int         | Likes count per day for first 30 days.                                                   |
| `day_1_comments` … `day_30_comments` | int         | Comments count per day for first 30 days.                                                |

### Notes
- All timestamps (`published_at`, `inserted_at`, and daily counters) are measured in **UTC**.
- Daily counters (`day_1_*` … `day_30_*`) represent values relative to the publish date.
- `tags` column is stored as a stringified list; users should parse into arrays for analysis.
- Historical YouTube fields like `favourite_count` are often zero and may be deprecated.
