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
ext = "csv"
csvdatafile = "offense_codes"
infile = os.path.join(datapath, csvdatafile + '.' + ext)
table = csvdatafile

df = pd.read_csv(infile)
df.head()
#%%
from sqlalchemy import create_engine
import pymysql
#%%
sqlengine = create_engine(
    'mysql+pymysql://{user}:{pw}@{host}/{db}'.format(user = rcred.user, 
                                                            pw = rcred.passwd, 
                                                            host = rcred.host, 
                                                            db = rcred.db), 
                                                            pool_recycle=3600)
sqlconnect = sqlengine.connect()

try:
    frame = df.to_sql(table, sqlconnect, if_exists='append');
except ValueError as vx:
    print(vx)
except Exception as ex:   
    print(ex)
else:
    print("Data appended successfully to table %s."%table);   
finally:
    sqlconnect.close()
    print("yeye")

#%%
