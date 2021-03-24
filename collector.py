from datetime import datetime

import influxdb_client
import time
from influxdb_client.client.write_api import SYNCHRONOUS
from psutil import sensors_battery, cpu_percent, swap_memory
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
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=data)
    return


def collect_data():
    data = []
    battery_level = get_battery_level()
    if battery_level:
        data.append(battery_level)
    data.append(get_cpu_usage())
    data.append(swap_memory_used())
    return data


def get_cpu_usage():
    cpu_usage = cpu_percent(interval=1)
    return influxdb_client.Point("cpu").field("CPU Percent", cpu_usage).tag("host_name", gma() + "").time(time.time_ns())


def get_battery_level():
    try:
        battery_level = sensors_battery()
        point = influxdb_client.Point("sensors").field("Battery Level", battery_level.percent).tag("host_name", gma() + "").time(time.time_ns())
    except AttributeError:
        return False
    return point


def swap_memory_used():
    swap_used = swap_memory()
    return influxdb_client.Point("memory").tag("host_name", gma() + "").field("Swap memory used", swap_used.percent).time(time.time_ns())
