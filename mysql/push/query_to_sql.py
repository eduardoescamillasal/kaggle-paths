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
import MySQLdb 
import fnmatch
import os

db = MySQLdb.connect(host=rcred.host,
                     user=rcred.user,
                     passwd=rcred.passwd,
                     db=rcred.db)
cursor = db.cursor()

path = os.path.dirname(os.path.abspath(__file__))
print(path)
print(os.path.join(path, "data"))
for file in os.listdir(os.path.join(path, "data")):
	if fnmatch.fnmatch(file,'*.csv'):
		print(file)
		fileparts = file.split('.')
		table = fileparts[0]
		Query = """ LOAD DATA LOCAL INFILE 'data/%s' \
		INTO TABLE %s \
		FIELDS TERMINATED BY ';' \
		LINES TERMINATED BY '\n' \
		IGNORE 1 ROWS; """ % (file, table)
		cursor.execute(Query) 
		db.commit()
cursor.close()

#%%
