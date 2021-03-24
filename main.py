import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import psutil
import time
from dotenv import load_dotenv
import os
import socket

load_dotenv()

batteryLevel = psutil.sensors_battery()

hostname = socket.gethostname()  # nomDeLaMachine
local_ip = socket.gethostbyname(hostname)  # ipDeLaMachine

print(psutil.cpu_percent(interval=1))

BUCKET = os.getenv("BUCKET")
ORG = os.getenv("ORG")
TOKEN = os.getenv("INFLUXDB_TOKEN")
# Store the URL of your InfluxDB instance
URL = os.getenv("URL")

client = influxdb_client.InfluxDBClient(
    url=URL,
    token=TOKEN,
    org=ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)


def test():
    batteryLevel = psutil.sensors_battery()
    cpuPercent = psutil.cpu_percent(interval=1)
    point = influxdb_client.Point("sensors").field("Battery Level", batteryLevel.percent).tag("host_name",
                                                                                              local_ip + "")
    write_api.write(bucket=BUCKET, org=ORG, record=point)
    point = influxdb_client.Point("cpu").field("CPU Percent", cpuPercent).tag("host_name", local_ip + "")
    write_api.write(bucket=BUCKET, org=ORG, record=point)
    time.sleep(1)
    print(batteryLevel.percent)
    print(cpuPercent)
    test()


test()
