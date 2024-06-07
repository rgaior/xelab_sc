import influxdb_client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "xelab_sc"
org = "xelab"
token = "hj0aom10LZKCNnDesgn0QrPCvz2pixID-i90f_RRHmw6rGrh_dL2q9EHKloPFIKUuU-PzzlaWLDI69gyuH2DjA=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"
write_api = client.write_api(write_options=SYNCHRONOUS)


client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
    org=org
)



def celsius_to_kelvin(tempC):
    return tempC + 273.15

#def decode_payload(measurement, data_dict,tags=None):
#{'from': 'lakeshore_105813', 'timestamp': 1717676421.744527, 'payload': {'TEMP_A': 295.82, 'TEMP_B': 0.0, 'HTR_1': 0.0, 'HTR_2': 0.0, 'RANGE1': 0.0, 'RANGE2': 0.0}}    
    

def push_to_influx(measurement, data_dict,tags=None):
    time = data_dict['timestamp']*1e9    
    to_push = {"measurement":measurement,
               "tags": tags,
               "fields":data_dict['payload'],
               "time": time,
               }
    print(f"to push {to_push}")
    # # query_api = client.query_api()
    # print("data = ", key, val)
    # _point1 = Point(measurement_name).tag("board",key[0]).tag("sensor",key[1]).tag("fault",val[1]).field("temp",float(val[0]))
    # write_api.write(bucket=bucket, record=[_point1])
    

    # # Use default dictionary structure
    #             dict_structure = {
    #                 "measurement": "h2o_feet",
    #                 "tags": {"location": "coyote_creek"},
    #                 "fields": {"water_level": 1.0},
    #                 "time": 1
    #             }
    #             point = Point.from_dict(dict_structure, WritePrecision.NS)
