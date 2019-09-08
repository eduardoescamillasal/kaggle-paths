import sensordata

sensordata.fetch_sensor_data()
datasets = sensordata.read_csvfiles()
metadata = sensordata.metadata_list()
n = len(datasets[0])
