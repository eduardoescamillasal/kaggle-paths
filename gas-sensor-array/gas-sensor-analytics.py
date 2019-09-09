#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sensordata
sns.set()

sensordata.fetch_sensor_data()
datasets = sensordata.read_csvfiles()
metadata = sensordata.metadata_list()
n = len(datasets[0])

#%%
sns.set_style(style='whitegrid')
fig, axes = plt.subplots(4,1, figsize=(17,12))
start = 0
stop = start + 500
sns.scatterplot(x=datasets[0].Time[start:stop], y=datasets[0].HeaterState[start:stop], ax=axes[0])
sns.scatterplot(x=datasets[0].Time[start:stop], y=datasets[0].Ticks[start:stop], ax=axes[1])
sns.scatterplot(x=datasets[0].Time[start:stop], y=datasets[0].HeatingCycle[start:stop], ax=axes[2])
sns.scatterplot(x=datasets[0].Time[start:stop], y=datasets[0].CycleLength[start:stop], ax=axes[3])
plt.show()

#%%
datasets[0]["HeatingCycle"], datasets[0]["CycleLength"] = sensordata.cyclegenerator(datasets[0])

#%%
colsind = sensordata.metadata_list()[2]
col = colsind["Time"]

#%%
fig, axes = plt.subplots(2,2, figsize=(25,10))
sensor = "R09"

sns.scatterplot(data=datasets[0],
                y=datasets[0][sensor][datasets[0].CycleLength == 25],
                x=datasets[0]["HeatingCycle"][datasets[0].CycleLength == 25],
                hue="CO",
                ax=axes[0,0])

sns.scatterplot(data=datasets[0],
                y=datasets[0][sensor][datasets[0].CycleLength == 25],
                x=datasets[0]["HeatingCycle"][datasets[0].CycleLength == 25],
                hue="Humidity",
                ax=axes[1,0])

sns.scatterplot(data=datasets[0],
                y=datasets[0][sensor][datasets[0].CycleLength == 20],
                x=datasets[0]["HeatingCycle"][datasets[0].CycleLength == 20],
                hue="CO",
                ax=axes[0,1])

sns.scatterplot(data=datasets[0],
                y=datasets[0][sensor][datasets[0].CycleLength == 20],
                x=datasets[0]["HeatingCycle"][datasets[0].CycleLength == 20],
                hue="Humidity",
                ax=axes[1,1])

plt.show()

#%%
