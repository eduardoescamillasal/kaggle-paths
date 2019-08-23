#%%
import os, sys
basepath = "/home/dreuter/Github/kaggle-paths"
global scriptpath
scriptpath = os.path.join(basepath,'mysql','push')
global csvpath
csvpath = os.path.join(scriptpath, "data")
global credpath;
credpath = os.path.join(basepath,"mysql",".cred")

os.chdir(scriptpath)
print(os.getcwd())

#%%

def connectsql():
	sys.path.append(credpath)
	import rcred
	from sqlalchemy import create_engine
	import pymysql
	sqlengine = create_engine('mysql+pymysql://{user}:{pw}@{host}/{db}'.format(user = rcred.user, 
																					 pw = rcred.passwd,
																					 host = rcred.host,
																					 db = rcred.db),
																					 pool_recycle=3600)
	sqlconnect = sqlengine.connect()
	return sqlconnect

def pushcsv(file):
	import pandas as pd
	sqlconnect = connectsql()
	table = file.split('.')[0]
	df = pd.read_csv(os.path.join(csvpath, file))
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

def loopcsv():
	import fnmatch
	for file in os.listdir(csvpath):
		table = file.split('.')[0]
		if fnmatch.fnmatch(file,'*.csv'):
			print(file + " is now being targeted to table " + table + ".")
			pushcsv(file)

if __name__ == "__main__":
	loopcsv()