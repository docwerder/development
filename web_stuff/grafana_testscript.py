from influxdb import InfluxDBClient

record = [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "Float_value": 0.64,
                "Int_value": 3,
                "String_value": "Text",
                "Bool_value": True
            }
        }
    ]

client = InfluxDBClient(host='192.168.178.48', port=8086, username='admin', password='123pax123', database='DBONE')

client.write_points(record)