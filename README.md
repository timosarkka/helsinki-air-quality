# Helsinki Air Quality Data Pipeline

## 1. Introduction

This project is a data engineering pipeline using Airflow, Snowflake and dbt. It ingests open air quality data from different locations in Helsinki via a python script and stores it in Snowflake. All the data is openly available through the Finnish Meteorological Institute (FMI) API, accessible here: https://en.ilmatieteenlaitos.fi/open-data

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

## 3. Tech Stack

My tech stack for this project:

- **Airflow**: Orchestrates the ETL pipeline
- **Snowflake**: Cloud data warehouse for storing and processing data
- **dbt**: Transforms and models data for analytics
- **Python**: Used for data extraction from the FMI API

## 4. Data Pipeline Architecture

A high level architecture diagram of the pipeline:

![image](https://github.com/user-attachments/assets/e32a1a31-2ff9-4655-bf96-f48624881bba)

1. The python-script calls the FMI API and fetches the air quality data from the last 12 hours.
2. The data is saved to the raw layer of a Snowflake database.
3. A dbt job runs 5 minutes after the data arrives on the Snowflake raw layer, transforms the data and saves it to the analytics layer.
4. The whole pipeline is orchestrated with Apache Airflow, which runs the pipeline 2x a day, or every 12 hours.

Details of each section are explained below.

## 5. Extracting Data

The Airflow DAG (`dags/run_extract_fmi_aq.py`) triggers a Python script (`extract/fmi_aq_ingest_daily.py`) to fetch air quality data from the FMI API twice a day. Each API call contains data from the last 12 hours, so we don't need to call the API constantly.

The Python script sends a request to the FMI API and retrieves XML data. ElementTree is used for parsing the data, element by element, into a pandas dataframe. The dataframe is then written into a Snowflake database's raw-layer.

## 6. Transforming Data

The dbt model (`transform/fmi_air_quality_transformed.sql`) performs several transformations to the data:
  - Splits coordinate data into latitude and longitude.
  - Converts time values into timestamps.
  - Cleans parameter names.
  - Filters out invalid data (e.g., NaN values).
  - Deduplicates records based on timestamp.
  
The last step is done in order to make sure that there are no duplicate records being written to the analytics layer. Technically, this is achieved by partitioning the raw layer by latitude, longitude, parameter and timestamp. Results are then ordered by timestamp, and only the latest record is being qualified for the analytics layer.

## 7. Loading Data

Finally, the transformed data is written to the Snowflake's analytics layer. The finalized dataset would be ready to be used e.g. for reporting and visualization.

## 8. Orchestration

Apache Airflow is used for automating the entire pipeline. Extract script runs 2x a day via an Airflow DAG. dbt transformations are triggered 5 minutes after data ingestion. The completion of pipeline jobs can also be monitored from the Airflow webserver.

## 9. Example of Data on Snowflake Analytics Layer

As an example, this is an extract of some of the data when transformed and ready to be used on the Snowflake analytics layer:

![Näyttökuva 2025-02-20 194011](https://github.com/user-attachments/assets/5834e0da-23fa-415d-b100-431b02af3098)

## 10. Future Work

A lot could still be done to improve this pipeline, this is just a basic implementation. Some things still to be done:

- Implement automated testing and data quality checks via dbt.
- Implement automated snapshotting of data via dbt.
- Record the actual locations of the coordinates to a seed file in dbt and join it to the data as an extra column.
- Expand the dataset to include more regions than only Helsinki.
- Visualize the dataset with Power BI.
