# Design Document – Medical X-Ray Data Engineering Pipeline

## Objective

The objective of this project is to build an end-to-end data engineering pipeline for Chest X-ray images that automatically ingests raw data, validates image files, quarantines invalid files, performs de-identification, transforms images into standardized formats, stores metadata, and generates execution logs.

## Dataset

This project uses the **Chest X-ray Images (Pneumonia)** public dataset from **Kaggle**.

* **Modality:** Chest X-ray
* **Format:** JPEG images
* **Classes:** NORMAL and PNEUMONIA
* **Demonstration Run:** 52 files processed (48 valid, 4 invalid/quarantined)

A sample subset of the dataset is included for demonstration, while the full dataset can be downloaded from Kaggle.

## Storage Layout

The pipeline follows a layered **Bronze–Silver–Gold** architecture.

| Layer         | Purpose                                                                  |
| ------------- | ------------------------------------------------------------------------ |
| `raw_data/`   | Original X-ray images downloaded from Kaggle                             |
| `landing/`    | Ingested copies before processing                                        |
| `silver/`     | Validated and standardized images resized to **512×512**                 |
| `gold/`       | ML-ready images resized to **224×224**, curated metadata, and thumbnails |
| `quarantine/` | Invalid or corrupted files                                               |
| `logs/`       | Pipeline execution logs                                                  |

This layered approach preserves raw data while producing clean, analysis-ready outputs.

## Metadata Schema

The pipeline extracts technical metadata from every valid image.

| Field       | Description                         |
| ----------- | ----------------------------------- |
| `record_id` | Anonymized unique record identifier |
| `filename`  | Image file name                     |
| `category`  | NORMAL or PNEUMONIA                 |
| `width`     | Original image width                |
| `height`    | Original image height               |
| `format`    | Image format                        |
| `status`    | Validation status                   |

The metadata is stored in:

* `metadata.csv`
* `gold/curated_metadata.csv`
* `metadata.db` (SQLite)

## Validation Strategy

Each file is validated using the **Pillow** library.

* Valid image files continue through the pipeline.
* Invalid or corrupted files are automatically moved to the `quarantine` folder.
* The pipeline records the number of valid and invalid files in the execution logs.

## De-identification Approach

The selected Kaggle dataset contains JPEG images without embedded patient identifiers such as patient names, dates of birth, or medical record numbers.

To maintain privacy:

* No patient-identifiable information is stored.
* Each record receives an anonymized `record_id`.
* Only technical image metadata is extracted and stored.

## Transformation Strategy

The pipeline creates multiple standardized versions of each valid image.

* **Silver Layer:** Images resized to **512×512** for standardized processing.
* **Gold Layer:** Images resized to **224×224** for machine learning readiness.
* **Thumbnails:** Images resized to **128×128** for quick preview and quality assurance.

These transformations create consistent outputs suitable for future analytics and AI workflows.

## Orchestration Choice

The pipeline uses a structured **Python script-based workflow**.

Execution order:

1. Data Ingestion
2. Validation
3. Quarantine Handling
4. De-identification
5. Image Transformation
6. Silver Layer Generation
7. Gold Layer Generation
8. Metadata Storage
9. Logging and Monitoring

A Python-based workflow was chosen because it is simple to implement, easy to rerun, and can later be extended to orchestration tools such as **Apache Airflow** or **Prefect**.

## Monitoring and Logging

The pipeline records important execution events using Python's `logging` module.

The logs include:

* Pipeline start
* Files processed
* Valid files
* Invalid files
* Quarantined files
* Pipeline completion

Logs are stored in:

`logs/pipeline.log`

## Limitations

* Uses local storage rather than cloud storage.
* Demonstration uses a small subset of the Kaggle dataset.
* JPEG images are used instead of DICOM medical imaging files.
* Script-based orchestration is used instead of Apache Airflow or Prefect.
* The pipeline is designed as a demonstration project and can be expanded for production use.
