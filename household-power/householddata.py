import os
import numpy as np
import pandas as pd

datadirname = 'data'
preprocdatadirname = 'preprocessed-data'
scriptpath = os.path.abspath(__file__)
scriptdir = os.path.dirname(scriptpath)
datapath = os.path.join(scriptdir,datadirname)

def load_and_preprocess_data():
    fetch_power_data()
    return load_power_data()

def attach_shifted_series(data, n_input=1, n_output=1, dropnan=True):
    n_pred = data.shape[1]
    dataframe = pd.DataFrame(data)
    cols, columns = [], []
    
    # append backward shifted predictor data to dataframe
    for i in range(n_input, 0, -1):
        cols.append(dataframe.shift(i))
        columns += [('col%d[t-%d]' % (j+1, i)) for j in range(n_pred)]
    
    # append forward shifted target data to dataframe
    for i in range(0, n_output):
        cols.append(dataframe.shift(-i))
        if i == 0:
            columns += [('target%d[t]' % (j+1)) for j in range(n_pred)]
        else:
            columns += [('target%d[t+%d]' % (j+1, i)) for j in range(n_pred)]
    
    aggregation = pd.concat(cols, axis=1)
    aggregation.columns = columns
    
    if dropnan:
        aggregation.dropna(inplace=True)
    return aggregation

def hour_of_day_average(powerdata):
    rooms = ["S1","S2","S3","S4"]
    roomdata = powerdata[rooms].resample("h").mean()
    n = len(roomdata)
    hoursaverage = np.zeros((3,24))
    for i in range(n):
        timefrom = roomdata.index[i]
        consumption = roomdata.iloc[i]
        hoursaverage[:,timefrom.hour]+=consumption
    return hoursaverage

def day_of_week_average(powerdata,weeksfromstart):
    rooms = ["S1","S2","S3","S4"]
    roomdata = powerdata[rooms].resample("D").mean()
    n = len(roomdata)
    dayofweekaverage = np.zeros((3,7))
    for i in range(n):
        timefrom = roomdata.index[i]
        consumption = roomdata.iloc[i]
        dayofweekaverage[:,timefrom.dayofweek]+=consumption
    return dayofweekaverage

def months_average(powerdata):
    rooms = ["S1","S2","S3","S4"]
    roomdata = powerdata[rooms].resample("M").mean()
    n = len(roomdata)
    monthsaverage = np.zeros((3,12))
    for i in range(n):
        timefrom = roomdata.index[i]
        consumption = roomdata.iloc[i]
        monthsaverage[:,timefrom.month-1]+=consumption
    return monthsaverage

def years_average(powerdata):
    rooms = ["S1","S2","S3","S4"]
    roomdata = powerdata[rooms].resample("Y").mean()
    n = len(roomdata)
    yearsaverage = np.zeros((4,5))
    for i in range(n):
        timefrom = roomdata.index[i]
        consumption = roomdata.iloc[i]
        yearsaverage[:,(timefrom.year-1)%5]+=consumption
    return yearsaverage

def daytimeframedata(powerdata,cols,day_of_interest):
    startdate = pd.Timestamp('2006-12-17 00:00')
    oneday = pd.Timedelta(days=1)
    dayshift = pd.Timestamp(startdate) + pd.Timedelta(days=day_of_interest)
    timefrom = pd.Timestamp(dayshift)
    timeto = pd.Timestamp(dayshift) + oneday

    return powerdata[cols][timefrom:timeto], timefrom

def convert_power_data(data):
    columns = metadata_list()[0]
    timefrom = '2006-12-16 17:24'
    timeto = '2010-11-26 21:03'
    timestamp = np.arange(timefrom, timeto,
                          np.timedelta64(1,'m'),
                          dtype='datetime64')
    powerdata = pd.DataFrame(data, index = timestamp, columns = columns)

    powerdata.GlobalActivePower = powerdata.GlobalActivePower.astype('float64')
    powerdata.GlobalActivePower = powerdata.GlobalActivePower.interpolate()

    powerdata.GlobalReactivePower = powerdata.GlobalReactivePower.astype('float64')
    powerdata.GlobalReactivePower = powerdata.GlobalReactivePower.interpolate()

    powerdata.Voltage = powerdata.Voltage.astype('float64')
    powerdata.Voltage = powerdata.Voltage.interpolate()

    powerdata.GlobalIntensity = powerdata.GlobalIntensity.astype('float64')
    powerdata.GlobalIntensity = powerdata.GlobalIntensity.interpolate()

    powerdata.S1 = powerdata.S1.astype('float64')
    powerdata.S1 = powerdata.S1.interpolate()

    powerdata.S2 = powerdata.S2.astype('float64')
    powerdata.S2 = powerdata.S2.interpolate()

    powerdata.S3 = powerdata.S3.astype('float64')
    powerdata.S3 = powerdata.S3.interpolate()
    
    powerdata["S4"] = (powerdata.GlobalActivePower * 1000 / 60) - (powerdata.S1 + powerdata.S2 + powerdata.S3)
    
    return powerdata

def load_power_data(datapath=datapath):
    powerconsumption_filename = metadata_list()[3][0]
    powerconsumption_filpath= os.path.join(datapath,powerconsumption_filename)
    powerconsumption_file = open(powerconsumption_filpath)
    powerconsumption_data = powerconsumption_file.read()
    powerconsumption_file.close()

    lines = powerconsumption_data.split('\n')

    columns = lines[0].split(';')
    values = lines[1:]
    n_values = len(values)

    data = []
    for i_row in range(n_values):
        row_split = values[i_row].split(';')
        row_len = len(row_split)
        if row_len == 9:
            if row_split[2] == '?':
                adjusted_rowsplit = row_split[:2] + [np.nan]*7
                data.append(adjusted_rowsplit)
            else:
                data.append(row_split)

    return convert_power_data(data)
    
def fetch_power_data(datapath=datapath):
    """Download and extract powerdata to data path location
    
    Keyword Arguments:
        datapath {string} -- Data path location on disk (default: {datapath})
    """
    import zipfile
    from six.moves import urllib
    file_url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip'

    if not os.path.isdir(datapath):
        print("Creating data directory " + datapath)
        os.makedirs("data")
    file_path = os.path.join(datapath, "power-data.zip")
    if not os.path.isfile(file_path):
        print("Downloading compressed data to: " + file_path)
        urllib.request.urlretrieve(file_url, file_path)
        print("Download succeded.")
    else:
        print(file_path + '\nalready exists, file not downloaded')
    checkfiles = 0
    for file in metadata_list()[3]:
        thiscsv = os.path.join(datapath,file)
        if not os.path.isfile(thiscsv):
            checkfiles = 1
    if checkfiles == 1:
        print("Extracting txt file to data directory ...")
        power_zip = zipfile.ZipFile(file_path,'r')
        power_zip.extractall(datapath)
        power_zip.close()
        print("Extraction done.")
    else:
        print('txt file already exists in\n' + datapath + ',\nno files extracted')

def metadata_list():
    """Holds some case specific metadata
    
    Returns:
        [objects] -- List of iterable metadata objects associated with the power consumption data analytics framework
        [objects][0] --> columns -- [{string}] -- List of column names for the analytics
        [objects][1] --> units -- [{string}] -- List of units used in columns
        [objects][2] --> colsind -- {{string: int}} -- Indexing directory for reverse column automation tasks
        [objects][3] --> txt_files -- [{string}] -- List of powerdata txt-files in this project
    """
    columns = ["Date", "Time",
               "GlobalActivePower", "GlobalReactivePower",
               "Voltage", "GlobalIntensity",
               "S1", "S2", "S3"]
    
    units = ['', '',
             'kW', 'kW',
             'V', 'A',
             'Wh','Wh', 'Wh']
    
    colsind = {'Date': 0, 'Time': 1,
               'GlobalActivePower': 2, 'GlobalReactivePower': 3,
               'Voltage': 4, 'GlobalIntensity': 5,
               'S1': 6, 'S2': 7, 'S3': 8}
    
    txt_files = ['household_power_consumption.txt']

    dayofweek = ['Monday','Tuesday','Wednesday',
                 'Thursday','Friday','Saturday','Sunday']
    
    months = ["Jan","Feb","Mar","Apr",
              "May","Jun","Jul","Aug",
              "Sep","Okt","Nov","Dec"]
    
    hourofday = [str(x) for x in range(24)]

    years = ["2006","2007","2008","2009","2010"]
    
    return [columns, units, colsind, txt_files, dayofweek, months, hourofday, years]