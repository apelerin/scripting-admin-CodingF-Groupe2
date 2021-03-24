import influxdb_client
import psutil
import time
import socket
from os import getenv
from influxdb_client.client.write_api import SYNCHRONOUS
from getmac import get_mac_address as gma
from dotenv import load_dotenv

load_dotenv()

batteryLevel = psutil.sensors_battery()

hostname = socket.gethostname()  # nomDeLaMachine
local_ip = socket.gethostbyname(hostname)  # ipDeLaMachine

BUCKET = getenv("BUCKET")
ORG = getenv("ORG")
TOKEN = getenv("INFLUXDB_TOKEN")
# Store the URL of your InfluxDB instance
URL = getenv("URL")

client = influxdb_client.InfluxDBClient(
    url=URL,
    token=TOKEN,
    org=ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)


def test():
    battery_level = psutil.sensors_battery()
    cpu_percent = psutil.cpu_percent(interval=1)
    try:
        point = influxdb_client.Point("sensors").field("Battery Level", battery_level.percent).tag("host_name",
                                                                                                   gma() + "")
        write_api.write(bucket=BUCKET, org=ORG, record=point)
    except AttributeError:
        pass
    point = influxdb_client.Point("cpu").field("CPU Percent", cpu_percent).tag("host_name", gma() + "")
    write_api.write(bucket=BUCKET, org=ORG, record=point)
    time.sleep(1)
    test()


test()
