#%%
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import powerdata
sns.set_style(style='whitegrid')

metadata = powerdata.metadata_list()
powerdataframe = powerdata.load_and_preprocess_data()
#%%
powerdataframe.head()

#%%
powerdataframe.info()

#%%
powerdataframe.describe()

#%%
startday = 27
timefrom = '2006-12-' + str(startday) + ' 00:00'
timeto = '2006-12-' + str(startday+1) + ' 00:00'
powerdataframe[["S1"]][timefrom:timeto].plot(figsize = (15,8))
plt.legend(fontsize=15)
plt.show()

#%%
metadata[2]["S3"]

#%%
