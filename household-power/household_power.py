#%%
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from householddata import load_and_preprocess_data
from householddata import metadata_list
from householddata import daytimeframedata
sns.set_style(style='whitegrid')

metadata = metadata_list()
dayofweek = metadata[4]
#%%
powerdata = load_and_preprocess_data()
#powerdata.head()
#powerdata.describe()
powerdata.info()
#%%
day_of_interest = 1 + 0*7
cols = ["S1"]
timeframedata, timefrom = timeframedata(powerdata,cols,day_of_interest)

timeframedata.plot(figsize = (15,8))
plt.legend(fontsize=15)
plt.show()
print(dayofweek[timefrom.dayofweek])
print("Total energy consumed in kitchen [kWh]")
print(np.sum(timeframedata)/1000)
#%%
metadata[2]["S3"]

#%%
onfilter = timeframedata > 0.00
np.sum(timeframedata)

#%%
np.sum(onfilter)

#%%
plt.figure(figsize = (15,8))
plt.scatter(np.arange(len(onfilter)),onfilter)
plt.show()
#%%
timefrom.dayofweek

#%%
