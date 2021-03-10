class importAsortyment(object):

	import pandas as pd
	import numpy as np
	import os.path
	from sqlalchemy import create_engine

	hostname="localhost"
	dbname="db"
	uname="root"
	pwd="testtest"

	engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
					.format(host=hostname, db=dbname, user=uname, pw=pwd))

	desired_width = 320

	pd.options.mode.chained_assignment = None
	pd.set_option('display.width', desired_width)
	np.set_printoptions(linewidth=desired_width)
	pd.set_option('display.max_columns',10)

	userhome = os.path.expanduser('~')
	excelfile = os.path.join(userhome, 'Desktop/magTermyv3', 'ASORTYMENT.xls')

	df = pd.read_excel(excelfile, skiprows=1)
	open(excelfile, "r")
	df = df.drop(['Unnamed: 0'], axis=1)
	df = df.drop(['Unnamed: 4'], axis=1)
	df = df.drop(['Unnamed: 5'], axis=1)
	df = df.drop(['Unnamed: 6'], axis=1)
	df = df.drop(['Unnamed: 7'], axis=1)
	df = df.drop(['Unnamed: 8'], axis=1)
	df = df.drop(['Unnamed: 9'], axis=1)
	df = df.drop(['Unnamed: 10'], axis=1)
	df = df.drop(['Unnamed: 11'], axis=1)
	df = df.drop(['Unnamed: 12'], axis=1)
	df = df.drop(['Unnamed: 13'], axis=1)
	df = df.drop(['Unnamed: 14'], axis=1)
	df = df.drop(['Unnamed: 15'], axis=1)
	df = df.drop(['Unnamed: 16'], axis=1)
	df = df.drop(['Unnamed: 17'], axis=1)
	df = df.drop(['Unnamed: 18'], axis=1)
	df = df.drop(['Unnamed: 19'], axis=1)
	df = df.drop(['Unnamed: 20'], axis=1)
	df = df.drop(['Unnamed: 21'], axis=1)
	df = df.drop(['Unnamed: 22'], axis=1)
	df = df.drop(['Unnamed: 23'], axis=1)
	df = df.drop(['Unnamed: 25'], axis=1)
	df = df.drop(['Unnamed: 26'], axis=1)
	df = df.drop(['Unnamed: 27'], axis=1)
	df = df.drop(['Unnamed: 28'], axis=1)
	df = df.drop(['Unnamed: 29'], axis=1)
	df = df.drop(['Unnamed: 30'], axis=1)
	df = df.drop(['Unnamed: 31'], axis=1)
	df = df.drop(['Unnamed: 32'], axis=1)
	df = df.drop(['Unnamed: 33'], axis=1)
	df = df.drop(['Unnamed: 34'], axis=1)
	df = df.drop(['Unnamed: 35'], axis=1)
	df = df.drop(['Unnamed: 36'], axis=1)
	df = df.drop(['Unnamed: 37'], axis=1)
	df = df.drop(['Unnamed: 38'], axis=1)
	df = df.drop(['Unnamed: 39'], axis=1)
	df = df.drop(['Unnamed: 40'], axis=1)
	df = df.drop(['Unnamed: 41'], axis=1)
	df = df.drop(['Unnamed: 42'], axis=1)
	df = df.drop(['Unnamed: 43'], axis=1)
	df = df.drop(['Unnamed: 44'], axis=1)
	df = df.drop(['Unnamed: 45'], axis=1)
	df = df.drop(['Unnamed: 46'], axis=1)
	df = df.drop(['Unnamed: 47'], axis=1)
	df = df.drop(['Unnamed: 48'], axis=1)
	df = df.drop(['Unnamed: 49'], axis=1)
	df = df.drop(['Unnamed: 50'], axis=1)
	df = df.drop(['Unnamed: 51'], axis=1)
	df = df.drop(['Unnamed: 52'], axis=1)
	df = df.drop(['Unnamed: 53'], axis=1)
	df = df.drop(['Unnamed: 54'], axis=1)
	df = df.drop(['Unnamed: 55'], axis=1)
	df = df.drop(['Unnamed: 56'], axis=1)
	df = df.drop(['Unnamed: 57'], axis=1)
	df = df.drop(['Unnamed: 58'], axis=1)
	df = df.drop(['Unnamed: 59'], axis=1)
	df = df.drop(['Unnamed: 61'], axis=1)
	df = df.drop(['Unnamed: 62'], axis=1)
	df = df.drop(['Unnamed: 63'], axis=1)
	df.to_sql('asortyment', engine, index=False)