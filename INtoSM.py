import pandas as pd
import numpy as np
import os.path
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey

from sqlalchemy.sql import select, update, insert, text

hostname="localhost"
dbname="db"
dbname2="magTermyv3"
uname="root"
pwd="testtest"

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
					.format(host=hostname, db=dbname, user=uname, pw=pwd))
engine2 = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
					.format(host=hostname, db=dbname2, user=uname, pw=pwd))

metadata = MetaData(engine)
metadata2 = MetaData(engine2)


desired_width = 320

BO = Table('BO', metadata,
           Column('ID', Integer, primary_key=True),
           Column('Nazwa', String),
           Column('Ilosc', Float),
           Column('Jednostka', String),
           Column('WartoscNetto',Float),
           Column('CenaZakupu',Float)
           )
magBar = Table('MAG_BAR', metadata2,
           Column('ID', Integer, primary_key=True),
           Column('Nazwa', String),
           Column('Ilosc', Float),
           Column('Jednostka', String),
           Column('WartoscNetto',Float),
           Column('CenaZakupu',Float)
           )
magKuchnia = Table('MAG_KUCHNIA', metadata2,
           Column('ID', Integer, primary_key=True),
           Column('Nazwa', String),
           Column('Ilosc', Float),
           Column('Jednostka', String),
           Column('WartoscNetto',Float),
           Column('CenaZakupu',Float)
           )
magSklepReg = Table('MAG_SR', metadata2,
           Column('ID', Integer, primary_key=True),
           Column('Nazwa', String),
           Column('Ilosc', Float),
           Column('Jednostka', String),
           Column('WartoscNetto',Float),
           Column('CenaZakupu',Float)
           )


pd.options.mode.chained_assignment = None
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

userhome = os.path.expanduser('~')
excelfile = os.path.join(userhome, 'Desktop/magTermyv3', 'MAG_BAR.xls')
excelfile2 = os.path.join(userhome, 'Desktop/magTermyv3', 'MAG_KUCHNIA.xls')
excelfile3 = os.path.join(userhome, 'Desktop/magTermyv3', 'MAG_SR.xls')



def dataFrameFromSQL(path):

		df = pd.read_excel(path, skiprows=4, usecols=['Lp.', 'Nazwa'])

		open(excelfile, "r")

		df.rename(columns={'Unnamed: 5': 'Jedn.'}, inplace=True)
		df.rename(columns={'Ilość': 'Ilosc'}, inplace=True)
		df.rename(columns={'Lp.': 'ID'}, inplace=True)

		a = df[df.Nazwa != 'Nazwa']  # Jeśli kolumna Nazwa ma wartość Nazwa -> zmien na Nan

		a.dropna(subset=["Nazwa"], inplace=True)  # Jeśli kolumna Nazwa zawiera Nan -> wyjeboj
		a['Nazwa'] = a['Nazwa'].str.replace('( [(][0-9]*[/]*[0-9]*[)])', '')
		a['Ilosc'] = np.nan
		a['Ilosc'].astype(float)
		a['Jednostka'] = ""
		a['WartoscNetto'] = np.nan
		a['WartoscNetto'].astype(float)
		a['CenaZakupu'] = np.nan
		a['CenaZakupu'].astype(float)
		return a


bar = dataFrameFromSQL(excelfile)
kuchnia = dataFrameFromSQL(excelfile2)
sklepregionalny = dataFrameFromSQL(excelfile3)



bar.to_sql('MAG_BAR', engine2, index=False)
engine.execute('ALTER TABLE MAG_BAR ADD PRIMARY KEY (`ID`);')
kuchnia.to_sql('MAG_KUCHNIA', engine2, index=False)
engine.execute('ALTER TABLE MAG_KUCHNIA ADD PRIMARY KEY (`ID`);')
sklepregionalny.to_sql('MAG_SR', engine2, index=False)
engine.execute('ALTER TABLE MAG_SR ADD PRIMARY KEY (`ID`);')

metadata.create_all(engine2)

metadata.create_all(engine)
connection = engine2.connect()
connection2 = engine.connect()

def selectFrom(table):
    s = select([table])
    result = connection.execute(s)
    a = list(result)
    return a

f = select([BO])
result = connection2.execute(f)
sm = list(result)


mgBar = selectFrom(magBar)
mgKuchnia = selectFrom(magKuchnia)
mgSklepReg = selectFrom(magSklepReg)


for a in sm:
	for b in mgBar:
		if a[1]==b[1]:
				update_statement = magBar.update() \
					.where(magBar.c.Nazwa == a[1]) \
					.values(Ilosc=a[2],
							WartoscNetto=a[4],
							CenaZakupu=a[5],
							Jednostka=a[3]
							)
				connection.execute(update_statement)

	for c in mgKuchnia:
		if a[1]==c[1]:
				update_statement = magKuchnia.update() \
					.where(magKuchnia.c.Nazwa == a[1]) \
					.values(Ilosc=a[2],
							WartoscNetto=a[4],
							CenaZakupu=a[5],
							Jednostka=a[3]
							)
				connection.execute(update_statement)

	for d in mgSklepReg:
		if a[1]==d[1]:
				update_statement = magSklepReg.update() \
					.where(magSklepReg.c.Nazwa == a[1]) \
					.values(Ilosc=a[2],
							WartoscNetto=a[4],
							CenaZakupu=a[5],
							Jednostka=a[3]
							)
				connection.execute(update_statement)








