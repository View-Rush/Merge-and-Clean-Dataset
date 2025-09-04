# Merge-and-Clean-Dataset

This project merges data from an Aiven PostgreSQL database and a BigQuery database into a single CSV file.

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

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Update `config/config.yaml` with your database credentials and output path.

## Usage
Run the merge script:
```bash
python src/merge.py
```

## Customization
- Add your merging logic in `src/merge.py`.
- Place any additional scripts or modules in the `src/` directory.
