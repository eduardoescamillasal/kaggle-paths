# Module related to this dataset in this particular setting
# of temperature modulated MOX sensor data aquisition
# 13 days of measurments stored in 13 files
#
# //Daniel Reuter

import os
import numpy as np
import pandas as pd

datadirname = 'data'
preprocdatadirname = 'preprocessed-data'
scriptpath = os.path.abspath(__file__)
scriptdir = os.path.dirname(scriptpath)
datapath = os.path.join(scriptdir,datadirname)
preprocpath = os.path.join(scriptdir,preprocdatadirname)

def load_and_preprocess_data(validationset=False, savecsv=False, sensorset='FIS'):
    fetch_sensor_data()
    datasets, features_sets, target_sets = read_csvfiles(prepocess=True, validationset=validationset, sensorset=sensorset)
    metadata = metadata_list()
    if savecsv == True:
        generate_features_csv(features_sets, target_sets)
    return datasets, features_sets, target_sets, metadata

def postprocess_data(features, target):
    """[summary]
    
    Arguments:
        features {[type]} -- [description]
        target {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    print("Postprocessing data matrix into subtarget concentration samples ..")
    start = 0
    for elem in target:
        if elem > 1:
            break
        start+=1

    sampleset = features[start:]
    targetset = target[start:]
    n = len(sampleset)
    dims = sampleset.shape[1]
    experiment_matrix = []
    observation = []
    targets = []

    if n > 2050:
        cyclespersample = 40
    else:
        cyclespersample = 20

    for i in range(n):
        observation.append(sampleset[i])
        if (i+1)%cyclespersample == 0:
            flatobs = np.array(observation).reshape(dims*cyclespersample)
            experiment_matrix.append(flatobs)
            targets.append(targetset[i-1])
            observation = []
    

    if len(targets) < 100:
        flatobs = np.array(observation).reshape(dims*len(observation))
        experiment_matrix.append(flatobs)
        targets.append(targetset[i-1])

    targets = np.array(targets).reshape(100)
    experiment_matrix = np.array(pd.DataFrame(experiment_matrix).interpolate(axis=1))
    print("Postprocessing done.")
    return experiment_matrix, targets


def read_csvfiles(datapath=datapath, validationset=False, prepocess=False, sensorset='FIS'):
    """Reading sensor data from csv and stores the data in memory.
    
    Keyword Arguments:
        datapath {string} -- CSV files location on disk (default: {datapath})
        validationset {bool} -- Includes the experimental validation sets (default: {False})
        prepocess {bool} -- Whether to preprocess feature data (default: {False})
    
    Returns:
        [pd.Dataframe] -- List of Pandas dataframes with experimental sensor data
        or
        [pd.Dataframe], [pd.Dataframe], numpy.array

        [pd.Dataframe] -- List of Pandas dataframes with experimental sensor data
        [pd.Dataframe] -- List of Pandas dataframes with preprocessed sensor features data
        [numpy.array] -- List of numpy array with carbon monoxid target values for features data
    """
    import time
    start_time = time.time()
    
    datasets = []
    features_sets = []
    target_sets = []
    metadata = metadata_list()
    (columns, units, colsind) = (metadata[0], metadata[1], metadata[2])
    csvfiles = collect_csvfiles(datapath)

    for file in csvfiles:
            filepath = os.path.join(datapath,file)
            dataset = pd.read_csv(filepath)
            n = len(dataset)
            
            if prepocess == True:
                print("Starting to import and preprocess sensor data from " + file)
                dataset, features, target = feature_generator(dataset, prepocess=True, sensorset=sensorset)
                datasets.append(dataset)
                features_sets.append(features)
                target_sets.append(target)
            else:
                print("Starting to import sensor data from" + file)
                dataset = feature_generator(dataset)
                datasets.append(dataset)

            print(file + ' successfully imported')
            if validationset == False:
                break

    elapsed_time = time.time() - start_time
    print(' ')
    if validationset == True:
        print(str(len(csvfiles)) + ' csv files has been loaded in ' + str(elapsed_time) + ' seconds\n' \
              + 'with preprocessing set to: ' + str(prepocess))
    else:
        print('Calibration set only has been loaded in ' + str(elapsed_time) + ' seconds\nwith preprocessing' \
               + 'set to: ' + str(prepocess))
    
    if prepocess == True:
        return datasets, features_sets, target_sets
    else:
        return datasets

def fetch_sensor_data(datapath=datapath):
    """Download and extract sensordata to data path location
    
    Keyword Arguments:
        datapath {string} -- Data path location on disk (default: {datapath})
    """
    import zipfile
    from six.moves import urllib
    file_url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/00487/gas-sensor-array-temperature-modulation.zip'

    if not os.path.isdir(datapath):
        print("Creating data directory " + datapath)
        os.makedirs("data")
    file_path = os.path.join(datapath, "gas-sensor-data.zip")
    if not os.path.isfile(file_path):
        print("Downloading compressed data to: " + file_path)
        urllib.request.urlretrieve(file_url, file_path)
        print("Download succeded.")
    else:
        print(file_path + '\nalready exists, file not downloaded')
    checkcsv = 0
    for file in metadata_list()[3]:
        thiscsv = os.path.join(datapath,file)
        if not os.path.isfile(thiscsv):
            checkcsv = 1
    if checkcsv == 1:
        print("Extracting csv files to data directory ...")
        sensor_zip = zipfile.ZipFile(file_path,'r')
        sensor_zip.extractall(datapath)
        sensor_zip.close()
        print("Extraction done.")
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

def generate_features_csv(features_sets, target_sets, preprocpath=preprocpath):
    """[summary]
    
    Arguments:
        features_sets {[type]} -- [description]
        target_sets {[type]} -- [description]
    
    Keyword Arguments:
        scriptdir {[type]} -- [description] (default: {scriptdir})
    """
    preproc_dir = 'preprocessed-data'
    if not os.path.isdir(preprocpath):
        print("Creating preprocessed-data directory\n" + preprocpath)
        os.makedirs(preproc_dir)
    
    datapath = os.path.join(scriptdir,preproc_dir)
    
    n = len(features_sets)
    print("Starting generation of csv-files with preprocessed data ...")
    for i in range(n):
        features = features_sets[i] # Some sets have top row nans
        co_cons = target_sets[i]
        if i+1 < 10:
            features_filename = 'day0' + str(i+1) + '_features.csv'
            target_filename = 'day0' + str(i+1) + '_target.csv'
        else:
            features_filename = 'day' + str(i+2) + '_features.csv'
            target_filename = 'day' + str(i+2) + '_target.csv'
        np.savetxt(os.path.join(datapath,features_filename), features, delimiter=',', fmt='%f')
        np.savetxt(os.path.join(datapath,target_filename), co_cons, delimiter=',', fmt='%f')
    print("Preprocessed data csv-files stored in\n" + preprocpath)

def feature_generator(dataset, prepocess=False, sensorset='FIS'):
    """Adds feature columns to dataframe
    
    Arguments:
        dataset {pd.DataFrame} -- Pandas dataframe with sensordata

    Keyword Arguments:
        prepocess {bool} -- Whether to preprocess feature data (default: {False})
    
    Returns:
        pd.DataFrame -- New pandas dataframe with added columns
    """

    if prepocess == True:
        heatingcycle, signals, co_cons = cycle_manager(dataset, prepocess=True, sensorset=sensorset)
        dataset["HeatingCycle"] = heatingcycle
        features = signals
        target = co_cons

        dataset.columns = metadata_list()[0]
        return dataset, features, target
    else:
        heatingcycle = cycle_manager(dataset)
        dataset["HeatingCycle"] = heatingcycle
        dataset.columns = metadata_list()[0]
        return dataset

def cycle_manager(dataset, prepocess=False, sensorset='FIS'):
    """Handles periodic pattern extraction due to heater modulaton, collecting
       cyclic data as rows of observations (signals)
    
    Arguments:
        dataset {pd.DataFrame} -- Pandas dataframe with sensordata
    
    Keyword Arguments:
        prepocess {bool} -- Whether to preprocess feature data (default: {False})
    
    Returns:
        heatingcycle {numpy.array}, signals {[np.array]}, co_cons {np.array} -- ...
        or
        heatingcycle {numpy.array} -- ...

        heatingcycle -- Information of where (seconds) in the cycle sample was taken
        signals -- list of numpy arrays with cyclic signaldata
        co_cons -- list with median concentration for each cycle
    """
    dataset = np.array(dataset) # Converting to 2D array
    n = len(dataset)
    colsind = metadata_list()[2]
    timecol = colsind["Time"]
    heatcol = colsind["HeaterVoltage"]
    heatingcycle = np.zeros(n, dtype=float)
    time = 5.0

    if prepocess == True:
        carbcol = colsind["CO"]
        signal_cycle = []
        co_cycle = []
        co_cons = []
        signals = []
        signalfilterval = 57
        heaterfilterval = 0.21
        if sensorset == 'FIG':
            SET = [6,7,8,9,10,11,12]
            samplepart = 0
        elif sensorset == 'FIS':
            SET = [13,15,16,17,18,19] # Sensor 14 is malfunctioning
            samplepart = 1
        elif sensorset == 'ALL':
            SET = [6,7,8,9,10,11,12,13,15,16,17,18,19] # Sensor 14 is malfunctioning
            samplepart = 2
        else:
            SET = [13]
            samplepart = 1

    for i in range(n - 1):
        heatingcycle[i] = time
        deltatime = dataset[i+1,timecol] - dataset[i,timecol]
        time += deltatime

        if (prepocess == True) and (dataset[i,heatcol] < heaterfilterval): # filter out heating period
            sensorsignals = dataset[i,SET] # Selected sensors
            signal_cycle.append(sensorsignals)
            co_cycle.append(dataset[i,carbcol])

        thisheat = dataset[i,heatcol]
        nextheat = dataset[i+1,heatcol]
        if (thisheat < 0.5) and (nextheat >= 0.5): # heater transition state

            if (prepocess == True):
                signal_cycle.append(sensorsignals)
                signal_cycle = np.array(signal_cycle) # Convert list of numpy vectors into 2D array
                signal_length = len(signal_cycle)

                if samplepart == 0:
                    samplebool = (signal_length < signalfilterval)
                elif samplepart == 1:
                    samplebool = (signal_length > signalfilterval)
                else:
                    samplebool = True

                if samplebool: # keep only one sensor type -- < 57 FIG > 57 FIS
                    if sensorset == 'ALL':
                        signal_cycle = signal_cycle[:40] # cut out 5s part that differs between sensors
                    signal_cycle = signal_cycle[:-3] # Cut edges with noise
                    dims = signal_cycle.shape[0]*signal_cycle.shape[1]
                    flatcycle = signal_cycle.reshape(dims) # flat out cycle data spanning the whole row
                    transformedsignals = np.log(1/flatcycle) # log transform ...
                    co_cycle.append(dataset[i,carbcol])
                    signals.append(np.array(transformedsignals))
                    co_cons.append(np.median(co_cycle))

                co_cycle = []
                signal_cycle = []
            
            time=0.0
            heatingcycle[i] = time
            deltatime = dataset[i+1,timecol] - dataset[i,timecol]
            time += deltatime
    if prepocess == True:
        co_cons = np.array(pd.DataFrame(co_cons))
        signals = np.array(pd.DataFrame(signals).interpolate(axis=1))
        print("The shape of features matrix is:")
        print(signals.shape)
        return heatingcycle, signals, co_cons
    else:
        return heatingcycle

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