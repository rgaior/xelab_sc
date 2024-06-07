import influxdb_client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "xelab_sc"
org = "xelab"
token = "hj0aom10LZKCNnDesgn0QrPCvz2pixID-i90f_RRHmw6rGrh_dL2q9EHKloPFIKUuU-PzzlaWLDI69gyuH2DjA=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"


client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)   

def push_to_influx(measurement, data_dict,tags={}):
    my_time = int(data_dict['timestamp']*1e9)
    to_push = {"measurement":measurement,
               "tags":tags,
               "fields": data_dict['payload'],
               "time": my_time
               }
    
    point = Point.from_dict(to_push)
    write_api.write(bucket=bucket, record=point)
    
