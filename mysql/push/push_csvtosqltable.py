#%%
import os, sys
basepath = "/home/dreuter/Github/kaggle-paths"
scriptpath = os.path.join(basepath,'mysql','push')
os.chdir(scriptpath)
print(os.getcwd())

credpath = os.path.join(scriptpath,"cred")
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

tablename = datafile[0]
sqlEngine = create_engine('mysql+pymysql://%s:%s@%s/%s'%(rcred.user,rcred.password,rcred.host,rcred.db), pool_recycle=3600)
dbConnection = sqlEngine.connect()

try:
    frame = df.to_sql(tablename, dbConnection, if_exists='fail');
except ValueError as vx:
    print(vx)
except Exception as ex:   
    print(ex)
else:
    print("Table %s created successfully."%tablename);   
finally:
    dbConnection.close()
#%%

#import MySQLdb
#dbConnection = MySQLdb.connect(host=rcred.host,
#                     user=rcred.user,
#                     passwd=rcred.password,
#                     db=rcred.db)
#cursor = dbConnection.cursor()

#Query = """ LOAD DATA INFILE 'pmsm_temperature_data.csv' \
#INTO TABLE quandata_test \
#FIELDS TERMINATED BY ';' \
#LINES TERMINATED BY '\n' \
#IGNORE 1 ROWS; """

#cursor.execute(Query)
#dbConnection.commit()
#cursor.close()
#dbConnection.close()
