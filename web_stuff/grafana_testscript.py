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


{"Time":"2023-05-15T15:09:53","ENERGY":{"TotalStartTime":"2023-04-28T15:07:49","Total":3.674,"Yesterday":0.093,"Today":0.072,"Period":0,"Power":7,"ApparentPower":17,"ReactivePower":16,"Factor":0.38,"Voltage":237,"Current":0.072}}

{"Time":"2023-05-15T15:09:53","ENERGY":{"TotalStartTime":"2023-04-28T15:07:49","Total":3.674,"Yesterday":0.093,"Today":0.072,"Period":0,"Power":7,"ApparentPower":17,"ReactivePower":16,"Factor":0.38,"Voltage":237,"Current":0.072}}