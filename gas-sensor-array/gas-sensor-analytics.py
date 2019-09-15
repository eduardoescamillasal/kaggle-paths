#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sensordata
sns.set_style(style='whitegrid')

datasets, features_sets, target_sets, metadata = sensordata.load_and_preprocess_data(validationset=True)
calibrationset = datasets[0]
calibration_features_matrix = features_sets[0]
calibration_co_cons = target_sets[0]

#%%
n = len(dataset)
ticks = np.zeros(n, dtype=int)
for i in range(n - 1):
    thisvalue = dataset["HeaterVoltage"][i]
    nextvalue = dataset["HeaterVoltage"][i+1]
    if (thisvalue >= 0.5) and (nextvalue < 0.5):
        ticks[i] = 1

#%%
len(dataset)/25

#%%
dataset.iloc[80:90]
dataset.head()

#%%
sns.set_style(style='whitegrid')
fig, axes = plt.subplots(4,1, figsize=(17,12))
start = 0
stop = start + 500
sns.scatterplot(x=dataset.Time[start:stop], y=dataset.Ticks[start:stop], ax=axes[1])
sns.scatterplot(x=dataset.Time[start:stop], y=dataset.HeatingCycle[start:stop], ax=axes[2])
plt.show()

#%%
colsind = sensordata.metadata_list()[2]
col = colsind["Time"]

#%%
fig, axes = plt.subplots(2,2, figsize=(25,10))
sensor = "R09"

sns.scatterplot(data=dataset,
                y=dataset[sensor][dataset.CycleLength == 25],
                x=dataset["HeatingCycle"][datasets[0].CycleLength == 25],
                hue="CO",
                ax=axes[0,0])

sns.scatterplot(data=dataset,
                y=dataset[sensor][dataset.CycleLength == 25],
                x=dataset["HeatingCycle"][datasets[0].CycleLength == 25],
                hue="Humidity",
                ax=axes[1,0])

sns.scatterplot(data=dataset,
                y=dataset[sensor][dataset.CycleLength == 20],
                x=dataset["HeatingCycle"][dataset.CycleLength == 20],
                hue="CO",
                ax=axes[0,1])

sns.scatterplot(data=dataset,
                y=dataset[sensor][dataset.CycleLength == 20],
                x=dataset["HeatingCycle"][dataset.CycleLength == 20],
                hue="Humidity",
                ax=axes[1,1])

plt.show()

#%%
plt.figure(figsize=(15,10))
plt.hist(dataset["CO"], bins=40)
plt.show()

#%%
import collections
ctr = collections.Counter(dataset["CO"]).most_common()[:10]
concvals = []

for i in range(len(ctr)):
    concvals.append(ctr[i][0])
concvals.sort()
midpoints = []
for i in range(len(concvals)-1):
    midpoint = (concvals[i+1] + concvals[i])/2
    midpoints.append(midpoint)
midpoints.sort()

discreteco = np.zeros(n)
j=0
for i in range(n):
    for midpoint in midpoints:
        if dataset["CO"][i] < midpoint:
            discreteco[i] = concvals[j]
            break
        elif dataset["CO"][i] > midpoints[-1]:
            discreteco[i] = 20.0
            break
        j+=1
    j=0

plt.hist(discreteco)
plt.show()
#%%
pd.Series(discreteco).unique()
#%%
