import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import psutil
import time


batteryLevel = psutil.sensors_battery()

print(batteryLevel.percent)

bucket = "etienne.buronfosse's Bucket"
org = "etienne.buronfosse@edu.itescia.fr"
token = "8ir7A_gX_SEHX872iiXVGCcEGQNhlXLGSPSKSjjj-ndk9X10JfgDq5NWF091v9GqKuj4fFM-CclJ5mTk3rLHzg=="
# Store the URL of your InfluxDB instance
url="https://westeurope-1.azure.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

def test():
    batteryLevel = psutil.sensors_battery()
    point = influxdb_client.Point("sensors").tag("host_name", "ordi_etienne").field("BatteryLevel", batteryLevel.percent)
    write_api.write(bucket=bucket, org=org, record=point)
    time.sleep(2) 
    print(batteryLevel.percent)
    test()

test()
