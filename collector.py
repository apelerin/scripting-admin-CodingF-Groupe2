from datetime import datetime

import influxdb_client
import time
from influxdb_client.client.write_api import SYNCHRONOUS
from psutil import sensors_battery, cpu_percent, swap_memory, disk_usage, disk_partitions
from getmac import get_mac_address as gma
from os import getenv
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler


def send_data(func):
    def wrapper():
        data = func()
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
    return wrapper


def collect_data():
    scheduler = BlockingScheduler(timezone='Europe/Paris')
    if sensors_battery() is not None:
        scheduler.add_job(get_battery_level, "interval", seconds=15)
    scheduler.add_job(get_cpu_usage, "interval", seconds=2)
    scheduler.add_job(swap_memory_used, "interval", seconds=10)
    scheduler.add_job(get_disk_usage, "interval", seconds=20)
    scheduler.start()


@send_data
def get_cpu_usage():
    cpu_usage = cpu_percent(interval=1)
    return influxdb_client.Point("cpu").field("CPU Percent", cpu_usage).tag("host_name", gma() + "").time(
        time.time_ns())


@send_data
def get_battery_level():
    battery_level = sensors_battery()
    if battery_level is not None:
        return influxdb_client.Point("sensors").field("Battery Level", battery_level.percent).tag("host_name",
                                                                                                   gma() + "").time(
            time.time_ns())


@send_data
def swap_memory_used():
    swap_used = swap_memory()
    return influxdb_client.Point("memory").tag("host_name", gma() + "").field("Swap memory used",
                                                                              swap_used.percent).time(time.time_ns())


@send_data
def get_disk_usage():
    disks = disk_partitions()
    for disk in disks:
        space_disk_usage = disk_usage(disk.device)
        yield influxdb_client.Point("disks").field("total", space_disk_usage.total).field("used", space_disk_usage.used)\
            .field("free", space_disk_usage.free).field("percent", space_disk_usage.percent).tag("host_name", gma() + "").tag("disk_name", disk.device)
