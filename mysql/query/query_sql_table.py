#%%
import os, sys
basepath = "/home/dreuter/Github/kaggle-paths"
scriptpath = os.path.join(basepath,'mysql','query')
os.chdir(scriptpath)
print(os.getcwd())

credpath = os.path.join(basepath,"mysql",".cred")
sys.path.append(credpath)
import rcred
#%%
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# ====== Connection ====== #
# Connecting to MySQL by providing a sqlachemy engine
# SQLAlchemy URI looks like this : 'mysql+mysqlconnector://user:password@host_ip:port/database'
sqlengine = create_engine(
    'mysql+mysqlconnector://{user}:{pw}@{host}:{port}/{db}'.format(user = rcred.user,
                                                            pw = rcred.password,
                                                            host = rcred.host,
                                                            port = rcred.port,
                                                            db = rcred.db),
                                                            pool_recycle=3600)
sqlconnect = sqlengine.connect()
#%%
# ====== Reading table ====== #
# Reading MySQL table into a pandas DataFrame
sqltable = "helloworld"
df = pd.read_sql('SELECT * FROM {table}'.format(table = sqltable), sqlconnect)
sqlconnect.close()
df.head()
#%%
df.info()
#%%
