import os
import numpy as np
import pandas as pd

datadirname = 'data'

scriptpath = os.path.abspath(__file__)
scriptdir = os.path.dirname(scriptpath)

file_url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/00487/gas-sensor-array-temperature-modulation.zip'
datapath = os.path.join(scriptdir,datadirname)

def fetch_sensor_data(file_url=file_url, datapath=datapath):
    """Download and extract sensordata to data path location
    
    Keyword Arguments:
        file_url {string} -- Compressed sensor data file url (default: {file_url})
        datapath {string} -- Data path location on disk (default: {datapath})
    """
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
    """Find and match csv files in data directory
    
    Keyword Arguments:
        datapath {string} -- Data path location on disk (default: {datapath})
    
    Returns:
        [{string}] -- List of csv files located at data path location
    """
    import fnmatch
    csvfiles = []; datasets = []
    for file in os.listdir(datapath):
        if fnmatch.fnmatch(file,'*.csv'):
            csvfiles.append(file)
    csvfiles.sort()
    return csvfiles

def read_csvfiles(datapath=datapath, timeindex=False, validationset=False):
    """Reading sensor data from csv and stores the data in memory.
    
    Keyword Arguments:
        datapath {string} -- CSV files location on disk (default: {datapath})
        timeindex {bool} -- Toggle time index being used (default: {False})
        validationset {bool} -- Includes the experimental validation sets (default: {False})
    
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
    
    return datasets

def heaterstategenerator(dataset):
    n = len(dataset)
    colsind = metadata_list()[2]
    col = colsind["HeaterVoltage"]
    heaterstate = np.zeros(n, dtype='int64')
    i = 0
    for state in np.array((dataset.iloc[:,col] > 0.5)):
        if state:
            heaterstate[i] = 1
        else:
            heaterstate[i] = 0
        i+=1
    return heaterstate

def ticksgenerator(dataset):
    n = len(dataset)
    ticks = np.zeros(n, dtype=int)
    for i in range(n - 1):
        thisvalue = dataset["HeaterState"][i]
        nextvalue = dataset["HeaterState"][i+1]
        if (thisvalue == 0) and (nextvalue == 1):
            ticks[i] = 1
    return ticks

def cyclegenerator(dataset):
    n = len(dataset)
    colsind = metadata_list()[2]
    col = colsind["Time"]
    heatingcycle = np.zeros(n)
    cyclelength = np.zeros(n, dtype='int64')
    leavecycle = False
    cycletracker = 1
    i = 0
    while i < n:
        cycletracker = (cycletracker+1)%2
        time = 5.0
        if i == 0:
            while dataset["Ticks"].iloc[i] == 0:
                heatingcycle[i] = time
                cyclelength[i] = 25
                deltatime = dataset.iloc[i+1,col] - dataset.iloc[i,col]
                time += deltatime
                i+=1
        
        if dataset["Ticks"].iloc[i] == 1 or leavecycle == True:
            if leavecycle == True:
                i+= -1
            if cycletracker == 0:
                cyclelength[i] = 20
            else:
                cyclelength[i] = 25
            leavecycle = False
            time = 0.0
            heatingcycle[i] = time
            i+=1
            while dataset["Ticks"].iloc[i] == 0:
                deltatime = dataset.iloc[i,col] - dataset.iloc[i-1,col]
                time += deltatime
                if cycletracker == 0:
                    cyclelength[i] = 20
                    heatingcycle[i] = (time)
                else:
                    cyclelength[i] = 25
                    heatingcycle[i] = (time)
                
                i+=1
                leavecycle = True
                if i == n:
                    deltatime = dataset.iloc[i-1,col] - dataset.iloc[i-2,col]
                    time += deltatime
                    heatingcycle[i-1] = (time)%cyclelength[i-1]
                    break
        i+=1

    return (heatingcycle, cyclelength)

def featuregenerator(dataset):
    columns = metadata_list()[0]
    colsind = metadata_list()[2]

    dataset["HeaterState"] = heaterstategenerator(dataset)
    dataset["Ticks"] = ticksgenerator(dataset)
    dataset["HeatingCycle"], dataset["CycleLength"] = cyclegenerator(dataset)

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

def simpleplot(dep,
               indep,
               data,
               columns,
               units,
               figsize = (10,7),
               ylim = (0, 0),
               xlim = (0, 0),
               kind = 'plot'):
    """Just a simple plot
    
    Arguments:
        dep {int} -- [description]
        indep {int} -- [description]
        data {array} -- [description]
        columns {[string]} -- [description]
        units {[string]} -- [description]
    
    Keyword Arguments:
        figsize {tuple} -- [description] (default: {(10,7)})
        ylim {tuple} -- [description] (default: {(0, 0)})
        xlim {tuple} -- [description] (default: {(0, 0)})
        kind {str} -- [description] (default: {'plot'})
    
    Returns:
        [type] -- [description]
    """
    import matplotlib.pyplot as plt
    if xlim != (0, 0):
        x = data.iloc[xlim[0]:xlim[1],indep]
        y = data.iloc[xlim[0]:xlim[1],dep]
    elif ylim != (0,0):
        x = data.iloc[ylim[0]:ylim[1],indep]
        y = data.iloc[ylim[0]:ylim[1],dep]
    else:
        x = data.iloc[:,indep]
        y = data.iloc[:,dep]
    
    fig, ax = plt.subplots(figsize=figsize)
    if kind == 'scatter':
        ax.plot(x,y, marker='.', linestyle='none')
    else:
        ax.plot(x,y, marker='.', linestyle='-')
    
    ax.set_title(columns[dep] + ' against ' + columns[indep])
    ax.set_ylabel(columns[dep] + ' [' + units[dep] + ']', size=13)
    ax.set_xlabel(columns[indep] + ' [' + units[indep] + ']', size=13)

    return fig, ax