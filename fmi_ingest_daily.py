import requests
import pandas
import xml.etree.ElementTree as ET

def fetch_air_quality_data():
    url = 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::airquality::hourly::simple&region=helsinki'
    response = requests.get(url)
    airq_output = response.text
    return airq_output

def parse_air_quality_data():
    root = ET.fromstring(xml_data)
    namespace = {'gml': 'http://www.opengis.net/gml/3.2'}
    records = []

xml_data = fetch_air_quality_data()
parsed_data = parse_air_quality_data(xml_data)