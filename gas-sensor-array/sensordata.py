import sys, os

datadirname = 'data'

scriptpath = os.path.abspath(__file__)
scriptdir = os.path.dirname(scriptpath)

file_url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/00487/gas-sensor-array-temperature-modulation.zip'
datapath = os.path.join(scriptdir,datadirname)

def fetch_sensor_data(file_url=file_url, datapath=datapath):
    import zipfile
    from six.moves import urllib
    if not os.path.isdir(datapath):
        os.makedirs("data")
    file_path = os.path.join(datapath, "gas-sensor-data.zip")
    if not os.path.isfile(file_path):
        urllib.request.urlretrieve(file_url, file_path)
    else:
        print(file_path + '\nalready exists in\n' + datapath + ',\nfile not downloaded')
    checkcsv = 0
    for file in metadata_list()[3]:
        thiscsv = os.path.join(datapath,file)
        if not os.path.isfile(thiscsv):
            checkcsv = 1
    if checkcsv == 1:
        sensor_zip = zipfile.ZipFile(file_path,'r')
        sensor_zip.extractall(datapath)
        sensor_zip.close()
    else:
        print('csv files already exists in\n' + datapath + ',\nno files extracted')

def collect_csvfiles(datapath=datapath):
    import fnmatch
    csvfiles = []; datasets = []
    for file in os.listdir(datapath):
        if fnmatch.fnmatch(file,'*.csv'):
            csvfiles.append(file)
    csvfiles.sort()
    return csvfiles

def read_csvfiles_with_timestamp(datapath=datapath):
    import time
    import numpy as np
    import pandas as pd
    start_time = time.time()
    csvfiles = collect_csvfiles(datapath)
    
    datasets = []
    for file in csvfiles:
            filepath = os.path.join(datapath,file)
            dataset = pd.read_csv(filepath)

            timestamps = []
            datetime = file.split('.csv')[0].split('_')
            datetime_string = datetime[0] + ' - ' + datetime[1]
            start_timestamp = pd.Timestamp(datetime_string)
            (columns, units, colsind) = (metadata_list()[0], metadata_list()[1], metadata_list()[2])
            
            for time in dataset.iloc[:,0]:
                timedelta = pd.Timedelta(seconds=time)
                thistime = start_timestamp + timedelta
                timestamps.append(thistime)
            dataset.index = timestamps

            dataset[colsind["HeaterState"]] = np.zeros(len(dataset), dtype='int64')
            dataset[colsind["Ticks"]] = np.zeros(len(dataset), dtype='int64')
            dataset[colsind["HeatingCycle"]] = np.zeros(len(dataset))
            dataset[colsind["CycleLength"]] = np.zeros(len(dataset), dtype='int64')
            dataset.columns = columns

            datasets.append(dataset)
            print(file + ' successfully imported')

    elapsed_time = time.time() - start_time
    print(' ')
    print(str(len(csvfiles)) + ' Data has been loaded in ' + str(elapsed_time) + ' seconds')
    return datasets

def read_csvfiles(datapath=datapath, timeindex=False, validationset=False):
    import time
    import numpy as np
    import pandas as pd
    start_time = time.time()
    
    datasets = []
    metadata = metadata_list()
    (columns, units, colsind) = (metadata[0], metadata[1], metadata[2])
    csvfiles = collect_csvfiles(datapath)

    for file in csvfiles:
            filepath = os.path.join(datapath,file)
            dataset = pd.read_csv(filepath)
            
            if timeindex == True:
                timestamps = []
                datetime = file.split('.csv')[0].split('_')
                datetime_string = datetime[0] + ' - ' + datetime[1]
                start_timestamp = pd.Timestamp(datetime_string)
            
                for timestamp in dataset.iloc[:,0]:
                    timedelta = pd.Timedelta(seconds=timestamp)
                    thistime = start_timestamp + timedelta
                    timestamps.append(thistime)
                dataset.index = timestamps

            dataset[colsind["HeaterState"]] = np.zeros(len(dataset), dtype='int64')
            dataset[colsind["Ticks"]] = np.zeros(len(dataset), dtype='int64')
            dataset[colsind["HeatingCycle"]] = np.zeros(len(dataset))
            dataset[colsind["CycleLength"]] = np.zeros(len(dataset), dtype='int64')
            dataset.columns = columns

            datasets.append(dataset)
            print(file + ' successfully imported')
            if validationset == False:
                break

    elapsed_time = time.time() - start_time
    print(' ')
    if validationset == True:
        print(str(len(csvfiles)) + ' csv files has been loaded in ' + str(elapsed_time) + ' seconds'
              + ' including validation sets')
    else:
        print('Calibration set only has been loaded in ' + str(elapsed_time) + ' seconds with time index'
               + ' set to: ' + str(timeindex))
    
    return datasets

def metadata_list():
    columns = ['Time', 'CO', 'Humidity', 'Temperature',
               'FlowRate', 'HeaterVoltage', 'R01', 'R02',
               'R03', 'R04', 'R05', 'R06', 'R07',
               'R08', 'R09', 'R10', 'R11', 'R12',
               'R13', 'R14', 'HeaterState', 'Ticks', 'HeatingCycle', 'CycleLength']
    units = ['s', 'ppm', '%.r.h', '°C', 'mL/min', 'V',
             'MOhm','MOhm', 'MOhm', 'MOhm', 'MOhm', 'MOhm', 'MOhm',
             'MOhm','MOhm', 'MOhm', 'MOhm', 'MOhm', 'MOhm', 'MOhm',
             'Boolean', 'Boolean', 's', 's']
    colsind = {'Time': 0, 'CO': 1, 'Humidity': 2, 'Temperature': 3,
               'FlowRate': 4, 'HeaterVoltage': 5, 'R01': 6, 'R02': 7,
               'R03': 8, 'R04': 9, 'R05': 10, 'R06': 11, 'R07': 12,
               'R08': 13, 'R09': 14, 'R10': 15, 'R11': 16, 'R12': 17,
               'R13': 18, 'R14': 19, 'HeaterState': 20, 'Ticks': 21, 'HeatingCycle': 22,
               'CycleLength': 23}
    csv_files = ['20160930_203718.csv', '20161001_231809.csv', '20161003_085624.csv',
                 '20161004_104124.csv', '20161005_140846.csv', '20161006_182224.csv',
                 '20161007_210049.csv', '20161008_234508.csv', '20161010_095046.csv',
                 '20161011_113032.csv', '20161013_143355.csv', '20161014_184659.csv',
                 '20161016_053656.csv']
    return [columns, units, colsind, csv_files]
