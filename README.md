# Finnish Air Quality Data Pipeline

## 1. Introduction

I was curious about the air quality of my hometown, Helsinki. So I decided to do a quick data pipeline and analysis to research it. All the analyzed data is available for everyone through the Finnish Meteorological Institute (FMI) API, accessible here: https://en.ilmatieteenlaitos.fi/open-data

The project implements a data pipeline to extract, transform, and load (ETL) air quality data to Snowflake. The pipeline is automated using Apache Airflow and transformed using dbt before being visualized in Power BI. A separate Python-script is used for data extraction.

## 2. Project Structure

The project folders are structured as shown below. Obviously I have not provided config.ini for security reasons, but it's needed to make the necessary connection to Snowflake.

```
├── dags/
│   ├── run_extract_fmi_aq.py  # Airflow DAG for orchestrating ETL
├── extract/
│   ├── fmi_aq_ingest_daily.py  # Python script for extracting data from FMI API
├── transform/
│   ├── fmi_air_quality.sql  # dbt model for data transformation
├── config.ini  # Configuration file with Snowflake credentials
```

[EDITED UNTIL THIS FAR]

## 3. Tech Stack

My tech stack for this project:

- **Airflow**: Orchestrates the ETL pipeline
- **Snowflake**: Cloud data warehouse for storing and processing data
- **dbt**: Transforms and models data for analytics
- **Python**: Used for data extraction from the FMI API
- **Power BI**: Visualization and analytics of processed data

## 4. Data Pipeline Architecture

1. **Extract**: Fetches air quality data from FMI API and stores it in Snowflake (RAW schema)
2. **Transform**: Uses dbt to clean, deduplicate, and format the data (ANALYTICS schema)
3. **Load**: Transformed data is stored in Snowflake for further analysis
4. **Automate**: Airflow schedules and manages the entire ETL process

## 5. Extracting Data
- The Airflow DAG (`run_extract_fmi_aq.py`) triggers a Python script (`fmi_aq_ingest_daily.py`) to fetch air quality data from the FMI API every hour.
- The Python script:
  - Sends a request to the FMI API and retrieves XML data.
  - Parses the XML data into a structured Pandas DataFrame.
  - Loads the parsed data into Snowflake’s RAW schema.

## 6. Transforming Data
- The dbt model (`fmi_air_quality_transformed.sql`) performs transformations:
  - Splits coordinate data into latitude and longitude.
  - Converts time values into timestamps.
  - Cleans parameter names.
  - Filters out invalid data (e.g., NaN values).
  - Deduplicates records based on timestamp.

## 7. Loading Data
- Extracted raw data is initially stored in Snowflake’s RAW schema.
- Transformed and cleaned data is stored in the ANALYTICS schema.
- The final dataset is ready for reporting and visualization.

## 8. Automation
- Airflow automates the entire pipeline:
  - Extract script runs hourly via an Airflow DAG.
  - dbt transformations are triggered after data ingestion.
  - Future enhancements may include notifications for failures or monitoring improvements.

## 9. Results and Analysis
*(To be added: Power BI dashboard visualization.)*

## 10. Future Work
- Implement additional quality checks on data.
- Expand the dataset to include more regions.
- Optimize dbt transformations for performance.
- Automate Power BI dashboard updates.

---
This project demonstrates a fully automated data pipeline using modern data engineering tools, ensuring clean and structured air quality data for analytics.

