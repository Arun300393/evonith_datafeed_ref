from influxdb_client_3 import InfluxDBClient3, Point
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

def write_to_influxdb(config, validated_data):
    """
    Write validated data to InfluxDB.
    """
    client = InfluxDBClient3(
        host=config["influxdb"]["host"],
        token=TOKEN,
        org=config["influxdb"]["org"]
    )
    write_api = client.write_api()

    for data in validated_data:
        points = [
            Point(data.measurement)
            .tag("sensor", tag)
            .field("value", value)
            .time(data.timestamp)
            for tag, value in data.values.items()
        ]
        write_api.write(bucket=config["influxdb"]["bucket"], record=points)
