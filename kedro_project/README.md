# Data Pipeline Project

This Python project implements a data pipeline for processing healthcare-related data. It involves loading, cleaning, structuring, merging, and saving the data into MongoDB. The pipeline follows these steps:

1. Load raw data from various file formats (CSV, Parquet, Excel) into MongoDB.
2. Retrieve data from MongoDB.
3. Clean and structure the data for analysis.
4. Merge the cleaned and structured data into a unified dataset.
5. Save the final merged dataset back to MongoDB.

## Project Structure

/pipeline
    /tasks
        /load_data.py
        /load_data_from_mongo.py
        /clean_data.py
        /structure_data.py
        /merge_data.py
        /save_data.py




## Dependencies

This project requires the following Python libraries:

- `pandas` for data manipulation
- `pymongo` for interacting with MongoDB
- `openpyxl` for working with Excel files
- `pyarrow` or `fastparquet` for reading Parquet files

You can install these dependencies using `pip`:



## Functions Overview

### `load_raw_data()`
- Loads raw data into MongoDB from various sources:
  - CSV files (`patients.csv`, `patient_gender.csv`, `symptoms.csv`, `medications.csv`)
  - Parquet file (`encounters.parquet`)
  - Excel file (`conditions.xlsx`)

### `load_data_from_mongo_step()`
- Retrieves the raw data from MongoDB.

### `clean_and_structure_data()`
- Cleans the data by applying the `clean_data()` function.
- Structures specific datasets like patients and symptoms using their respective structure functions (`structure_patient_data()`, `structure_symptoms()`).

### `merge_all_data()`
- Merges the structured patient data, symptoms, encounters, medications, conditions, and patient gender into a unified dataset.

### `save_final_data()`
- Saves the final merged data into MongoDB.

### `run_pipeline()`
- Executes the entire pipeline in sequence: loading data, cleaning and structuring data, merging data, and saving the final dataset.

## How to Use

### Step 1: Configure File Paths

In the `load_raw_data()` function, modify the file paths as per your data sources.

### Step 2: Run the Pipeline

Execute the pipeline by running the following command:




kedro_project.py

This will trigger the full ETL process, from loading the raw data to saving the processed data into MongoDB.

### Step 3: Check MongoDB

Once the pipeline completes, check MongoDB for the `master_data` collection, which will contain the final merged dataset.

## Example

The following example shows how the pipeline is executed:

```python
if __name__ == "__main__":
    run_pipeline()


This will load data from the files specified, clean and structure it, merge it into one dataset, and store it in MongoDB.

Notes:
    Ensure that MongoDB is running and accessible before executing the pipeline.
    Giving MONGO DB URL in code is must to run pipeline.
    We can add more data transformation steps or additional sources based on project requirements.
