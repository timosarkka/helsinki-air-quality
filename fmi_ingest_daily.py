import requests

def fetch_air_quality_data():
    url = 'https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::airquality::hourly::simple&region=helsinki'
    response = requests.get(url)
    airq_output = response.text
    print(airq_output)

fetch_air_quality_data()