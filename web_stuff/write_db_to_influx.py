import pandas as pd

from influxdb import InfluxDBClient
from influxdb import DataFrameClient

# df = pd.DataFrame(data=list(range(30)),
#                   index=pd.date_range(start='2014-11-16', periods=30, freq='H'),
#                   columns=['0'])

# client = InfluxDBClient(host='192.168.178.48', port=8086, username='admin', password='123pax123', database='DBONE')
client = DataFrameClient(host='192.168.178.48', port=8086, username='admin', password='123pax123', database='DBONE')

df = pd.DataFrame(data=list(range(13)),index=pd.date_range(start='2014-11-16',periods=13, freq='H'),columns=['0'])
client.delete_series(database='DBONE', measurement='demo')
client.write_points(df, 'demo', protocol='line')
# client.write_points(df, 'demo',{'k1': 'v1', 'k2': 'v2'}, time_precision=None, protocol='json')

