#%%
import os, sys
basepath = "/home/dreuter/Github/kaggle-paths"
scriptpath = os.path.join(basepath,'mysql','query')
os.chdir(scriptpath)
print(os.getcwd())

credpath = os.path.join(scriptpath,'..',"cred")
sys.path.append(credpath)
import rcred
#%%
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# ====== Connection ====== #
# Connecting to mysql by providing a sqlachemy engine
sqlengine = create_engine('mysql+mysqlconnector://%s:%s@%s/%s'%(rcred.user,rcred.password,rcred.host,rcred.db), pool_recycle=3600)
sqlconnect = sqlengine.connect()
#%%
# ====== Reading table ====== #
# Reading Mysql table into a pandas DataFrame
sqltable = "bitstampUSD"
df = pd.read_sql('SELECT * FROM {table}'.format(table = sqltable), sqlconnect)
sqlconnect.close()
#%%
df.head()
#%%
df.info()
#%%
