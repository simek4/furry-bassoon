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
magBAR = os.path.join(userhome, 'Desktop/magTermyv3/inwentaryzacja', 'BAR_IN_3101.xls')
magKUCHNIA = os.path.join(userhome, 'Desktop/magTermyv3/inwentaryzacja', 'KUCHNIA_IN_3101.xls')
magSR = os.path.join(userhome, 'Desktop/magTermyv3/inwentaryzacja', 'SKLEP_IN_3101.xls')

# df = pd.read_excel(excelfile, skiprows=4)

#Magazyn Bar
df = pd.read_excel(magBAR, usecols=['Nazwa', 'Ilosc'])
open(magBAR, "r")
a = df
a['Ilosc'] = a['Ilosc'].astype(float)
df = pd.read_excel(magKUCHNIA, usecols=['Nazwa', 'Ilosc'])
open(magKUCHNIA, "r")
b = df
b['Ilosc'] = b['Ilosc'].astype(float)
df = pd.read_excel(magSR, usecols=['Nazwa', 'Ilosc'])
open(magSR, "r")
c = df
c['Ilosc'] = c['Ilosc'].astype(float)



a.to_sql('IN_BAR', engine, index=False)
b.to_sql('IN_KUCHNIA', engine, index=False)
c.to_sql('IN_SR', engine, index=False)




# engine.execute('ALTER TABLE RASklepSportowy ADD PRIMARY KEY (`Lp.`);')

# print(a.head(5000).to_string())
#print(b.head(5000).to_string())

