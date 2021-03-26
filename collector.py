from datetime import datetime

import influxdb_client
import time
from influxdb_client.client.write_api import SYNCHRONOUS
from psutil import (
    sensors_battery, cpu_percent, swap_memory, disk_usage, disk_partitions, virtual_memory, net_io_counters
)
from getmac import get_mac_address as gma
from os import getenv
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler


def send_data(func):
    """Send data to influxdb

    Args:
        func : function that retrieve some points
    Returns: the wrapper which writes points in influxdb
    """
    def wrapper():
        """The wrapper which makes the link to influx fb

        """
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
    """Call each function with their respective range

    """
    scheduler = BlockingScheduler(timezone='Europe/Paris')
    if sensors_battery() is not None:
        scheduler.add_job(get_battery_level, "interval", seconds=15)
    scheduler.add_job(get_cpu_usage, "interval", seconds=2)
    scheduler.add_job(get_swap_memory_used, "interval", seconds=10)
    scheduler.add_job(get_disk_usage, "interval", seconds=60)
    scheduler.add_job(get_virtual_memory, "interval", seconds=5)
    scheduler.add_job(get_network_data, "interval", seconds=10)
    scheduler.start()


@send_data
def get_cpu_usage():
    """Get CPU usage per second

    Returns: point object from influxdb-client
    """
    cpu_usage = cpu_percent(interval=1)
    return influxdb_client.Point("cpu").field("CPU Percent", cpu_usage).tag("host_name", gma() + "")


@send_data
def get_battery_level():
    """Get battery level

    Returns: point object from influxdb-client
    """
    battery_level = sensors_battery()
    if battery_level is not None:
        return influxdb_client.Point("sensors").field("Battery Level", battery_level.percent).tag("host_name", gma() + "")


@send_data
def get_swap_memory_used():
    """Get swap memory used

    Returns: point object from influxdb-client
    """
    swap_used = swap_memory()
    return influxdb_client.Point("memory").field("Swap memory used", swap_used.percent).tag("host_name", gma() + "")


@send_data
def get_disk_usage():
    """Get disks information

    Returns: list of points object from influxdb-client
    """
    disks = disk_partitions()
    for disk in disks:
        space_disk_usage = disk_usage(disk.device)
        yield influxdb_client.Point("disks")\
            .field("total", space_disk_usage.total)\
            .field("used", space_disk_usage.used)\
            .field("free", space_disk_usage.free)\
            .field("percent", space_disk_usage.percent)\
            .tag("host_name", gma() + "")\
            .tag("disk_name", disk.device)


@send_data
def get_virtual_memory():
    """Get virtual memory information

    Returns: point object from influxdb-client
    """
    memory = virtual_memory()
    return influxdb_client.Point("memory")\
        .field("total_virtual_memory", memory.total)\
        .field("virtual_memory_used", memory.used)\
        .field("virtual_memory_free", memory.free)\
        .tag("host_name", gma() + "")


@send_data
def get_network_data():
    """Get network information since system starts

    Returns: point object from influxdb-client
    """
    network_data = net_io_counters()
    return influxdb_client.Point("network")\
        .field("uploading", network_data.bytes_sent)\
        .field("downloading", network_data.bytes_recv)\
        .tag("host_name", gma() + "")
