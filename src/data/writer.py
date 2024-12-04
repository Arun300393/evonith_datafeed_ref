from influxdb_client import InfluxDBClient, Point

def write_to_influxdb(config, validated_data):
    """
    Write validated data to InfluxDB.
    """
    client = InfluxDBClient(
        url=config["influxdb"]["url"],
        token=config["influxdb"]["token"],
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
