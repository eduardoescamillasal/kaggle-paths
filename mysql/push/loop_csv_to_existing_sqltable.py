#%%
import os, sys
basepath = "/home/dreuter/Github/kaggle-paths"
scriptpath = os.path.join(basepath,'mysql','push')
os.chdir(scriptpath)
print(os.getcwd())

credpath = os.path.join(basepath,"mysql",".cred")
sys.path.append(credpath)
import rcred
#%%
import pandas as pd
import mysql.connector
import fnmatch
import os
from sqlalchemy import create_engine

sqlengine = create_engine(
    'mysql+mysqlconnector://{user}:{pw}@{host}/{db}'.format(user = rcred.user, 
                                                            pw = rcred.passwd, 
                                                            host = rcred.host, 
                                                            db = rcred.db), 
                                                            pool_recycle=3600)
sqlconnect = sqlengine.connect()

path = os.path.dirname(os.path.abspath(__file__))
csvpath = os.path.join(path, "data")
for file in os.listdir(csvpath):
	if fnmatch.fnmatch(file,'*.csv'):
		table = file.split('.')[0]
		print("Data from file '" + file + "' is now being pushed to table " + table + ".")
		df = pd.read_csv(os.path.join(csvpath, file))
		try:
			frame = df.to_sql(table, sqlconnect, if_exists='append');
		except ValueError as vx:
			print(vx)
		except Exception as ex:   
			print(ex)
		else:
			print("Table %s created successfully."%table);
sqlconnect.close()
