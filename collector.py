import influxdb_client
import time

from influxdb_client.client import write_api
from influxdb_client.client.write_api import SYNCHRONOUS
from psutil import sensors_battery, cpu_percent
from getmac import get_mac_address as gma
from os import getenv
from dotenv import load_dotenv


def send_data(data):
    load_dotenv()

    BUCKET = getenv("BUCKET")
    ORG = getenv("ORG")
    TOKEN = getenv("INFLUXDB_TOKEN")
    URL = getenv("URL")

    client = influxdb_client.InfluxDBClient(
        url=URL,
        token=TOKEN,
        org=ORG
    )
    return


def collect_data():
    battery_level = get_battery_level()
    cpu_usage = get_cpu_usage()
    if not battery_level:
        return
    return


def get_cpu_usage():
    cpu_usage = cpu_percent(interval=1)
    point = influxdb_client.Point("cpu").field("CPU Percent", cpu_usage).tag("host_name", gma() + "")
    return point


def get_battery_level():
    try:
        battery_level = sensors_battery()
        point = influxdb_client.Point("sensors").field("Battery Level", battery_level.percent).tag("host_name", gma() + "")
    except AttributeError:
        return False
    return point
