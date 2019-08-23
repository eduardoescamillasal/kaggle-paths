#%%
import os, sys
basepath = "/home/dreuter/Github/kaggle-paths"
scriptpath = os.path.join(basepath,'mysql','push')
os.chdir(scriptpath)
print(os.getcwd())

credpath = os.path.join(basepath,"mysql",".cred")
sys.path.append(credpath)
import rcred

datapath = os.path.join(scriptpath,"data")
#%%
import pandas as pd
datafile = ("crime_latest","csv")

datafilepath = os.path.join(datapath,"{filename}.{ext}".format(filename = datafile[0],ext = datafile[1]))
df = pd.read_csv(datafilepath)
df.head()
#%%
df.info()
#%%
from sqlalchemy import create_engine
import pymysql

# ====== Connection ====== #
# Connecting to MySQL by providing a sqlachemy engine
# SQLAlchemy URI looks like this : 'mysql+pymysql://user:password@host_ip:port/database'
sqlengine = create_engine(
    'mysql+pymysql://{user}:{pw}@{host}/{db}'.format(user = rcred.user, 
                                                            pw = rcred.passwd, 
                                                            host = rcred.host, 
                                                            db = rcred.db), 
                                                            pool_recycle=3600)
sqlconnect = sqlengine.connect()

# ====== Create Table and push data ====== #
# Creates table and pushing data to MySQL given that table dont already exist
table = datafile[0]
print("Targeting...")
try:
    frame = df.to_sql(table, sqlconnect, if_exists='fail');
except ValueError as vx:
    print(vx)
except Exception as ex:   
    print(ex)
else:
    print("Table %s created successfully."%table);   
finally:
    sqlconnect.close()


#%%
