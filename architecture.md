# X-Ray Data Pipeline Architecture

## Tools Used
- Python
- Pandas
- Pillow (PIL)
- SQLite
- Logging Module
- VS Code

## Data Flow

Raw X-Ray Dataset (50 Images)
        │
        ▼
raw_data (Bronze)
        │
        ▼
Data Ingestion
(Copy files to Landing)
        │
        ▼
landing
        │
        ▼
Validation
(Check image integrity)
        │
   ┌────┴────┐
   ▼         ▼
silver   quarantine
(256×256) (Invalid files)
   │
   ▼
gold (224×224)
   │
   ▼
Metadata Extraction
   ├── metadata.csv
   └── metadata.db (SQLite)
   │
   ▼
Logging
logs/pipeline.log