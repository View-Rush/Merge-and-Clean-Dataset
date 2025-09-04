# Merge-and-Clean-Dataset

This project merges data from an Aiven PostgreSQL database and a BigQuery database into a single CSV file. The process is automated using a GitHub Actions workflow.


## How to Run the GitHub Actions Workflow

### 1. Trigger the Workflow

1. Go to the **Actions** tab in your GitHub repository.
2. Select the **Merge Video Data** workflow.
3. Click **Run workflow** and confirm.

The workflow will:
- Set up Python and install dependencies
- Write the BigQuery credentials JSON to the file specified by `BIGQUERY_CREDENTIALS_PATH`
- Run the merge script (`src/merge.py`)
- Upload the merged CSV as an artifact

### 2. Download the Output
After the workflow completes, download the merged CSV from the workflow run's artifacts section.

---

## Setting Up Environment Variables (For Repository Maintainers)

If you are setting up this repository for the first time or managing secrets, add the following secrets in **Settings > Secrets and variables > Actions**:

- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `BIGQUERY_PROJECT_ID`
- `BIGQUERY_DATASET`
- `BIGQUERY_TABLE`
- `BIGQUERY_CREDENTIALS_PATH` (e.g., `gcp-key.json`)
- `BIGQUERY_CREDENTIALS_JSON` (paste the full JSON key for your GCP service account)

---

## Folder Structure

```
Merge-and-Clean-Dataset/
├── config/           # Configuration files (YAML, credentials)
│   └── config.yaml   # Database connection settings
├── data/             # Input/output data files
├── src/              # Source code
│   ├── __init__.py
│   ├── merge.py      # Main script to merge data
│   └── db_utils.py   # Database utility functions
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## Local Development (Optional)
You can also run the merge script locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Update `config/config.yaml` with your database credentials and output path.
3. Run:
   ```bash
   python src/merge.py
   ```
