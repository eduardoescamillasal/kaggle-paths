import os
import numpy as np
import pandas as pd

datadirname = 'data'
scriptpath = os.path.abspath(__file__)
scriptdir = os.path.dirname(scriptpath)
datapath = os.path.join(scriptdir,datadirname)

def fetch_sensor_data(datapath=datapath):
    """Download and extract sensordata to data path location
    
    Keyword Arguments:
        file_url {string} -- Compressed sensor data file url (default: {file_url})
        datapath {string} -- Data path location on disk (default: {datapath})
    """
    import zipfile
    from six.moves import urllib
    file_url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/00487/gas-sensor-array-temperature-modulation.zip'

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
    """Find and match csv files in data directory
    
    Keyword Arguments:
        datapath {string} -- Data path location on disk (default: {datapath})
    
    Returns:
        [{string}] -- List of csv files located at data path location
    """

    import fnmatch

    csvfiles = []
    datasets = []
    for file in os.listdir(datapath):
        if fnmatch.fnmatch(file,'*.csv'):
            csvfiles.append(file)
    csvfiles.sort()
    return csvfiles

def read_csvfiles(datapath=datapath, timeindex=False, validationset=False, prepocess=False):
    """Reading sensor data from csv and stores the data in memory.
    
    Keyword Arguments:
        datapath {string} -- CSV files location on disk (default: {datapath})
        timeindex {bool} -- Toggle time index being used (default: {False})
        validationset {bool} -- Includes the experimental validation sets (default: {False})
        prepocess {bool} -- Whether to preprocess feature data
    
    Returns:
        [pd.Dataframe] -- List of Pandas dataframes with experimental sensor data
    """
    import time
    start_time = time.time()
    
    datasets = []
    metadata = metadata_list()
    (columns, units, colsind) = (metadata[0], metadata[1], metadata[2])
    csvfiles = collect_csvfiles(datapath)

    for file in csvfiles:
            filepath = os.path.join(datapath,file)
            dataset = pd.read_csv(filepath)
            n = len(dataset)
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
            
            if prepocess == True:
                dataset, features, co_conc = featuregenerator(dataset, prepocess=True)
            else:
                dataset = featuregenerator(dataset)

            datasets.append(dataset)
            print(file + ' successfully imported')
            if validationset == False:
                break

    elapsed_time = time.time() - start_time
    print(' ')
    if validationset == True:
        print(str(len(csvfiles)) + ' csv files has been loaded in ' + str(elapsed_time) + ' seconds'
              + ' including validation sets with time index set to: ' + str(timeindex))
    else:
        print('Calibration set only has been loaded in ' + str(elapsed_time) + ' seconds with time index'
               + ' set to: ' + str(timeindex))
    
    if prepocess == True:
        return datasets, features, co_conc
    else:
        return datasets

def cyclemanager(dataset, prepocess=False):
    n = len(dataset)
    colsind = metadata_list()[2]
    timecol = colsind["Time"]
    heatcol = colsind["HeaterVoltage"]
    signalfilter = (dataset.iloc[:,heatcol] < 0.25) 
    signalset = dataset[signalfilter]
    
    heatingcycle = np.zeros(n, dtype=float)
    time = 5.0

    if prepocess == True:
        carbcol = colsind["CO"]
        cycle = arr = np.empty((0,7), float)
        co_cycle = []
        co_cons = []
        signals = []

    for i in range(n - 1):
        heatingcycle[i] = time
        deltatime = dataset.iloc[i+1,timecol] - dataset.iloc[i,timecol]
        time += deltatime

        if prepocess == True:
            sensorsignals = np.array(dataset.iloc[i,6:13]).reshape(1,7) #Figaro sensors
            cycle = np.append(cycle, sensorsignals, axis=0)
            co_cycle.append(dataset.iloc[i,carbcol])

        thisvalue = dataset.iloc[i,heatcol]
        nextvalue = dataset.iloc[i+1,heatcol]
        if (thisvalue < 0.5) and (nextvalue >= 0.5):

            if prepocess == True:
                cycle = np.append(cycle, sensorsignals, axis=0)
                cycle = cycle[20:65] # Euqal part log transform linear signal range
                dims = cycle.shape[0]*cycle.shape[1]
                co_cycle.append(dataset.iloc[i,carbcol])
                signals.append(np.log10(1/cycle.reshape(dims)))
                co_cons.append(np.mean(co_cycle))
                co_cycle = []
                cycle = arr = np.empty((0,7), float)
            
            time=0.0
            heatingcycle[i] = time
            deltatime = dataset.iloc[i+1,timecol] - dataset.iloc[i,timecol]
            time += deltatime
    if prepocess == True:
        return heatingcycle, signals, co_cons
    else:
        return heatingcycle

def featuregenerator(dataset, prepocess=False):
    """Adds feature columns to dataframe
    
    Arguments:
        dataset {pd.DataFrame} -- Pandas dataframe with sensordata
    
    Returns:
        pd.DataFrame -- New pandas dataframe with added columns
    """

    if prepocess == True:
        heatingcycle, signals, co_cons = cyclemanager(dataset, prepocess)
        dataset["HeatingCycle"] = heatingcycle
        features = np.array(pd.DataFrame(signals))
        dataset.columns = metadata_list()[0]
        return dataset, features, co_cons
    else:
        heatingcycle = cyclemanager(dataset, prepocess)
        dataset["HeatingCycle"] = heatingcycle
        dataset.columns = metadata_list()[0]
        return dataset

def metadata_list():
    """Holds some case specific metadata
    
    Returns:
        [objects] -- List of iterable metadata objects associated with the sensor data analytics framework
        [objects][0] --> columns -- [{string}] -- List of column names for the analytics
        [objects][1] --> units -- [{string}] -- List of units used in columns
        [objects][2] --> colsind -- {{string: int}} -- Indexing directory for reverse column automation tasks
        [objects][3] --> csv_files -- [{string}] -- List of sensordata csv-files in this project
    """
    columns = ['Time', 'CO', 'Humidity', 'Temperature',
               'FlowRate', 'HeaterVoltage', 'R01', 'R02',
               'R03', 'R04', 'R05', 'R06', 'R07',
               'R08', 'R09', 'R10', 'R11', 'R12',
               'R13', 'R14', 'HeatingCycle']
    units = ['s', 'ppm', '%.r.h', '°C', 'mL/min', 'V',
             'MOhm','MOhm', 'MOhm', 'MOhm',
             'MOhm', 'MOhm', 'MOhm', 'MOhm','MOhm',
             'MOhm', 'MOhm', 'MOhm', 'MOhm', 'MOhm', 's']
    colsind = {'Time': 0, 'CO': 1, 'Humidity': 2, 'Temperature': 3,
               'FlowRate': 4, 'HeaterVoltage': 5, 'R01': 6, 'R02': 7,
               'R03': 8, 'R04': 9, 'R05': 10, 'R06': 11, 'R07': 12,
               'R08': 13, 'R09': 14, 'R10': 15, 'R11': 16, 'R12': 17,
               'R13': 18, 'R14': 19, 'HeatingCycle': 21}
    csv_files = ['20160930_203718.csv', '20161001_231809.csv', '20161003_085624.csv',
                 '20161004_104124.csv', '20161005_140846.csv', '20161006_182224.csv',
                 '20161007_210049.csv', '20161008_234508.csv', '20161010_095046.csv',
                 '20161011_113032.csv', '20161013_143355.csv', '20161014_184659.csv',
                 '20161016_053656.csv']
    
    return [columns, units, colsind, csv_files]