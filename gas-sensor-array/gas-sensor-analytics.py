import sensordata

sensordata.fetch_sensor_data()
datasets = sensordata.read_csvfiles(timeindex=False)
metadata = sensordata.metadata_list()
n = len(datasets[0])