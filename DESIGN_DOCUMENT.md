# Design Document – X-Ray Data Engineering Pipeline

## Objective

Build an end-to-end data engineering pipeline for Chest X-Ray images that ingests raw data, validates files, transforms images, stores metadata, and generates execution logs.

## Dataset

- Chest X-Ray Images (Pneumonia)
- Sample size: 50 images
- 25 NORMAL
- 25 PNEUMONIA

## Storage Layout

The project follows a Bronze–Silver–Gold architecture.

- raw_data (Bronze): Original images.
- landing: Ingested copies before processing.
- silver: Standardized images resized to 256×256.
- gold: Curated images resized to 224×224.
- quarantine: Invalid or corrupted files.
- logs: Pipeline execution logs.

## Metadata Schema

The metadata contains:

| Field | Description |
|-------|-------------|
| filename | Image file name |
| category | NORMAL or PNEUMONIA |
| width | Original image width |
| height | Original image height |
| format | Image format |

Metadata is stored in:

- metadata.csv
- metadata.db (SQLite)

## Validation Strategy

Each image is opened using Pillow.

- Valid images continue.
- Invalid or corrupted files are moved to the quarantine folder.

## De-identification

The selected dataset contains JPEG images without patient-identifiable metadata such as patient name, date of birth, or medical record number.

Therefore:

- No patient identifiers are stored.
- Only technical metadata is extracted.

## Transformation

Images are standardized into two versions.

- Silver: 256×256
- Gold: 224×224

This makes the dataset consistent for future analytics or machine learning.

## Orchestration Choice

The pipeline uses a Python script-based workflow.

Reasons:

- Simple implementation.
- Easy to rerun.
- Suitable for small datasets.
- Can be extended to Airflow or Prefect later.

## Monitoring

The logging module records:

- Pipeline start
- Files copied
- Valid files
- Invalid files
- Pipeline completion

Logs are stored in:

logs/pipeline.log

## Limitations

- Local storage only.
- Small sample dataset.
- JPEG images instead of DICOM.
- Script-based orchestration instead of Airflow.