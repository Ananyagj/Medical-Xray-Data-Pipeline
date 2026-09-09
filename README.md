# End-to-End X-Ray Data Engineering Pipeline

## Project Overview

This project builds an end-to-end data engineering pipeline for Chest X-Ray images using Python. The pipeline ingests raw images, validates them, transforms them into standardized formats, stores metadata, and generates logs.

## Dataset

- Dataset: Chest X-Ray Images (Pneumonia)
- Sample Used: 50 images (25 NORMAL + 25 PNEUMONIA)

## Technologies Used

- Python 3.14
- Pandas
- Pillow (PIL)
- SQLite
- Logging Module
- VS Code

## Folder Structure

Medical-Xray-Data-Pipeline/
├── raw_data/
├── landing/
├── quarantine/
├── silver/
├── gold/
├── logs/
├── metadata.csv
├── metadata.db
├── pipeline.py
├── architecture.md
└── README.md

## Pipeline Stages

1. Data Ingestion
2. Validation
3. Transformation
4. Metadata Extraction
5. Bronze/Silver/Gold Storage
6. SQLite Metadata Storage
7. Logging
8. Re-runnable Pipeline

## How to Run

1. Open the project in VS Code.
2. Activate the virtual environment.
3. Run:

python pipeline.py

## Output Files

- landing/ – copied raw files
- silver/ – resized 256×256 images
- gold/ – resized 224×224 images
- metadata.csv – extracted metadata
- metadata.db – SQLite database
- logs/pipeline.log – execution logs

## Assumptions

- JPEG X-Ray images are used.
- No patient-identifiable metadata exists in the sample dataset.

## Limitations

- Processes a small sample (50 images).
- Uses a local folder instead of cloud storage.
- Uses a script-based pipeline instead of Airflow.