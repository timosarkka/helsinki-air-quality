import configparser
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine

# Load configuration file
config = configparser.ConfigParser()
config.read('../config.ini')

# Get credentials from config
sf = config['snowflake']
user = sf['user']
password = sf['password']
account = sf['account']
warehouse = sf['warehouse']
database = sf['database']
schema = sf['schema']
role = sf['role']

# Make API call and fetch the XML-data as a string
def fetch_air_quality_data():
    url = 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::airquality::hourly::simple&region=helsinki'
    response = requests.get(url)
    return response.text

# Parse data from XML to DataFrame
def parse_aq_data_to_df(xml_data):
    namespaces = {
        "wfs": "http://www.opengis.net/wfs/2.0",
        "BsWfs": "http://xml.fmi.fi/schema/wfs/2.0",
        "gml": "http://www.opengis.net/gml/3.2"
    }

    # Get the root tag and initialize empty list for saving row-level data
    root = ET.fromstring(xml_data)
    data = []

    # Loop through the nested XML members and extract needed data
    for member in root.findall("wfs:member", namespaces):
        element = member.find("BsWfs:BsWfsElement", namespaces)
        if element is not None:
            coords = element.find("BsWfs:Location/gml:Point/gml:pos", namespaces)
            time = element.find("BsWfs:Time", namespaces)
            param_name = element.find("BsWfs:ParameterName", namespaces)
            param_value = element.find("BsWfs:ParameterValue", namespaces)
            data.append([coords.text.strip(), time.text, param_name.text, param_value.text])

    # Save to DataFrame and return it
    df = pd.DataFrame(data, columns=['COORDINATES', 'TIME', 'PARAMETER', 'VALUE'])
    return df

def write_to_snowflake(parsed_df):
    connection_string = (f'snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}')
    engine = create_engine(connection_string)
    parsed_df.to_sql(name='fmi_air_quality', con=engine, if_exists='append', index=False)

# Main function
def main():
    xml_data = fetch_air_quality_data()
    print("Fetched data from FMI API successfully.")
    parsed_df = parse_aq_data_to_df(xml_data)
    print("Converted data to a DataFrame successfully.")
    write_to_snowflake(parsed_df)
    print("Data was written to Snowflake schema RAW successfully.")

main()