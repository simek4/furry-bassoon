import pandas as pd
import numpy as np
import os.path
from sqlalchemy import create_engine
import re

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
excelfile = os.path.join(userhome, 'Desktop/RA', '0106-1506.xls')
# excelfile2 = os.path.join(userhome, 'Desktop/RA', '1606-2406.xls')
# excelfile3 = os.path.join(userhome, 'Desktop/RA', '2506-3006.xls')
# excelfile4 = os.path.join(userhome, 'Desktop/RA', '0107-0507.xls')
# excelfile5 = os.path.join(userhome, 'Desktop/RA', '0607-1007.xls')
# excelfile6 = os.path.join(userhome, 'Desktop/RA', '1107-1407.xls')
# excelfile7 = os.path.join(userhome, 'Desktop/RA', '1507-1707.xls')
# excelfile8 = os.path.join(userhome, 'Desktop/RA', '1807-2007.xls')
# excelfile9 = os.path.join(userhome, 'Desktop/RA', '2107-2307.xls')
# excelfile10 = os.path.join(userhome, 'Desktop/RA', '2407-2507.xls')
# excelfile11 = os.path.join(userhome, 'Desktop/RA', '2607-2807.xls')
# excelfile12 = os.path.join(userhome, 'Desktop/RA', '2907-3107.xls')
# excelfile13 = os.path.join(userhome, 'Desktop/RA', '0108-0308.xls')
# excelfile14 = os.path.join(userhome, 'Desktop/RA', '0408-0608.xls')
# excelfile15 = os.path.join(userhome, 'Desktop/RA', '0708-0808.xls')
# excelfile16 = os.path.join(userhome, 'Desktop/RA', '0908-1108.xls')
# excelfile17 = os.path.join(userhome, 'Desktop/RA', '1208-1408.xls')
# excelfile18 = os.path.join(userhome, 'Desktop/RA', '1508-1608.xls')
# excelfile19 = os.path.join(userhome, 'Desktop/RA', '1708-1908.xls')
# excelfile20 = os.path.join(userhome, 'Desktop/RA', '2008-2208.xls')
# excelfile21 = os.path.join(userhome, 'Desktop/RA', '2308-2608.xls')
# excelfile22 = os.path.join(userhome, 'Desktop/RA', '2708-2908.xls')
# excelfile23 = os.path.join(userhome, 'Desktop/RA', '3008-0209.xls')
# excelfile24 = os.path.join(userhome, 'Desktop/RA', '0309-0609.xls')
# excelfile25 = os.path.join(userhome, 'Desktop/RA', '0709-1009.xls')
# excelfile26 = os.path.join(userhome, 'Desktop/RA', '1109-1309.xls')
# excelfile27 = os.path.join(userhome, 'Desktop/RA', '1409-1709.xls')
# excelfile28 = os.path.join(userhome, 'Desktop/RA', '1809-2009.xls')
# excelfile29 = os.path.join(userhome, 'Desktop/RA', '2109-2409.xls')
# excelfile30 = os.path.join(userhome, 'Desktop/RA', '2509-2809.xls')
# excelfile31 = os.path.join(userhome, 'Desktop/RA', '2909-0410.xls')
# excelfile32 = os.path.join(userhome, 'Desktop/RA', '0510-3110.xls')
# excelfile33 = os.path.join(userhome, 'Desktop/RA', '0111-3112.xls')

# excelfile = os.path.join(userhome, 'Desktop/Cytryny', 'BEEFEATERSPRITZ.xls')
# excelfile2 = os.path.join(userhome, 'Desktop/Cytryny', 'BLUELAGOON.xls')
# excelfile3 = os.path.join(userhome, 'Desktop/Cytryny', 'BOMBAYTONIC.xls')
# excelfile4 = os.path.join(userhome, 'Desktop/Cytryny', 'COSMOPOLITAN.xls')
# excelfile5 = os.path.join(userhome, 'Desktop/Cytryny', 'DAIQUIRITRUSKAWKOWE.xls')
# excelfile6 = os.path.join(userhome, 'Desktop/Cytryny', 'DIPGUAKAMOLE.xls')
# excelfile7 = os.path.join(userhome, 'Desktop/Cytryny', 'GINCASSISFIZZ.xls')
# excelfile8 = os.path.join(userhome, 'Desktop/Cytryny', 'GINTONIC.xls')
# excelfile9 = os.path.join(userhome, 'Desktop/Cytryny', 'GRANITA.xls')
# excelfile10 = os.path.join(userhome, 'Desktop/Cytryny', 'GREYGOOSELEMONADE.xls')
# excelfile11 = os.path.join(userhome, 'Desktop/Cytryny', 'HERBATA.xls')
# excelfile12 = os.path.join(userhome, 'Desktop/Cytryny', 'HERBATAEX.xls')
# excelfile13 = os.path.join(userhome, 'Desktop/Cytryny', 'HERBATAZESLIWOWICA.xls')
# excelfile14 = os.path.join(userhome, 'Desktop/Cytryny', 'HERBATAZIMOWA.xls')
# excelfile15 = os.path.join(userhome, 'Desktop/Cytryny', 'JOHNCOLLINS.xls')
# excelfile16 = os.path.join(userhome, 'Desktop/Cytryny', 'KAMIKAZEBLUE.xls')
# excelfile17 = os.path.join(userhome, 'Desktop/Cytryny', 'KAMIKAZERED.xls')
# excelfile18 = os.path.join(userhome, 'Desktop/Cytryny', 'KRYSTALICZNEZRODLO05PET.xls')
# excelfile19 = os.path.join(userhome, 'Desktop/Cytryny', 'LEMONIADA.xls')
# excelfile20 = os.path.join(userhome, 'Desktop/Cytryny', 'LILLETBLANCTONIC.xls')
# excelfile21 = os.path.join(userhome, 'Desktop/Cytryny', 'LILLETVIVE_1.xls')
# excelfile22 = os.path.join(userhome, 'Desktop/Cytryny', 'LONGISLANDICETEA.xls')
# excelfile23 = os.path.join(userhome, 'Desktop/Cytryny', 'LYNCHBURGLEMONADELB.xls')
# excelfile24 = os.path.join(userhome, 'Desktop/Cytryny', 'MAKOSERNIK.xls')
# excelfile25 = os.path.join(userhome, 'Desktop/Cytryny', 'MAKOSERNIKKG.xls')
# excelfile26 = os.path.join(userhome, 'Desktop/Cytryny', 'MARGHARITA.xls')
# excelfile27 = os.path.join(userhome, 'Desktop/Cytryny', 'MOJITOHAVANA.xls')
# excelfile28 = os.path.join(userhome, 'Desktop/Cytryny', 'OGORKOWOMIETOWY.xls')
# excelfile29 = os.path.join(userhome, 'Desktop/Cytryny', 'POMIDOROWOCHRZANOWY.xls')
# excelfile30 = os.path.join(userhome, 'Desktop/Cytryny', 'PURPLERAIN.xls')
# excelfile31 = os.path.join(userhome, 'Desktop/Cytryny', 'READYORNOT.xls')
# excelfile32 = os.path.join(userhome, 'Desktop/Cytryny', 'SALATKAZKURCZAKIEMSPA.xls')
# excelfile33 = os.path.join(userhome, 'Desktop/Cytryny', 'SALATKAZKURCZAKIEMIBEKONEM.xls')
# excelfile34 = os.path.join(userhome, 'Desktop/Cytryny', 'SOKCYTRYNA20ML.xls')
# excelfile35 = os.path.join(userhome, 'Desktop/Cytryny', 'SERNIKZSOSEMCZEKOLADOWYM.xls')
# excelfile36 = os.path.join(userhome, 'Desktop/Cytryny', 'SUROWKAZSELERA.xls')
# excelfile37 = os.path.join(userhome, 'Desktop/Cytryny', 'SUROWKAZMARCHEWKI.xls')
# excelfile38 = os.path.join(userhome, 'Desktop/Cytryny', 'WHISKYSOUR.xls')


def dataFrameFromSQL(path):
    df = pd.read_excel(path, usecols=['Chochołowskie Termy Sp. z o. o.'])
    df.dropna(subset=["Chochołowskie Termy Sp. z o. o."], inplace=True)
    getDate = df['Chochołowskie Termy Sp. z o. o.']

    for a in getDate:
        print(a)
        okDate = re.findall('([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])' , a)

        if not okDate:
            print("Pusto")
        else:
            fromDate = okDate[0]
            toDate = okDate[1]

    df = pd.read_excel(path, skiprows=4)
    df = df.drop(['Nazwa asortymentu'], axis=1)
    df = df.drop(['Ilość'], axis=1)
    df = df.drop(['Unnamed: 0'], axis=1)  # drop columny
    df = df.drop(['Unnamed: 2'], axis=1)
    df = df.drop(['Unnamed: 3'], axis=1)
    df = df.drop(['Unnamed: 6'], axis=1)

    df.rename(columns={'Unnamed: 9': 'od'}, inplace=True)
    df.rename(columns={'Unnamed: 10': 'do'}, inplace=True)

    df['od']=fromDate
    df['do']=toDate

    df = df.drop(['Unnamed: 11'], axis=1)
    df = df.drop(['Unnamed: 13'], axis=1)
    df = df.drop(['Unnamed: 15'], axis=1)
    df = df.drop(['Unnamed: 17'], axis=1)
    df = df.drop(['Unnamed: 18'], axis=1)

    df.rename(columns={'Unnamed: 5': 'Nazwa asortymentu'}, inplace=True)
    df.rename(columns={'Unnamed: 8': 'Ilosc'}, inplace=True)

    df.dropna(subset=["Ilosc"], inplace=True)  # Jeśli kolumna Nazwa zawiera Nan -> wyjeboj

    df['Ilosc'] = df['Ilosc'].str.replace(' ', '')

    df['Ilosc'] = df['Ilosc'].str.replace(',', '.').astype(float)
    df['Netto'] = df['Netto'].str.replace(' ', '')
    df['Netto'] = df['Netto'].str.replace(',', '.').astype(float)
    df['Brutto'] = df['Brutto'].str.replace(' ', '')
    df['Brutto'] = df['Brutto'].str.replace(',', '.').astype(float)
    df['VAT'] = df['VAT'].str.replace(' ', '')
    df['VAT'] = df['VAT'].str.replace(',', '.').astype(float)
    df['Dokument'] = df['Dokument'].str.replace('( [(][0-9]*[/]*[0-9]*[)])', '')

    return df



a01 = dataFrameFromSQL(excelfile)
# a02 = dataFrameFromSQL(excelfile2)
# a03 = dataFrameFromSQL(excelfile3)
# a04 = dataFrameFromSQL(excelfile4)
# a05 = dataFrameFromSQL(excelfile5)
# a06 = dataFrameFromSQL(excelfile6)
# a07 = dataFrameFromSQL(excelfile7)
# a08 = dataFrameFromSQL(excelfile8)
# a09 = dataFrameFromSQL(excelfile9)
# a10 = dataFrameFromSQL(excelfile10)
# a11 = dataFrameFromSQL(excelfile11)
# a12 = dataFrameFromSQL(excelfile12)
# a13 = dataFrameFromSQL(excelfile13)
# a14 = dataFrameFromSQL(excelfile14)
# a15 = dataFrameFromSQL(excelfile15)
# a16 = dataFrameFromSQL(excelfile16)
# a17 = dataFrameFromSQL(excelfile17)
# a18 = dataFrameFromSQL(excelfile18)
# a19 = dataFrameFromSQL(excelfile19)
# a20 = dataFrameFromSQL(excelfile20)
# a21 = dataFrameFromSQL(excelfile21)
# a22 = dataFrameFromSQL(excelfile22)
# a23 = dataFrameFromSQL(excelfile23)
# a24 = dataFrameFromSQL(excelfile24)
# a25 = dataFrameFromSQL(excelfile25)
# a26 = dataFrameFromSQL(excelfile26)
# a27 = dataFrameFromSQL(excelfile27)
# a28 = dataFrameFromSQL(excelfile28)
# a29 = dataFrameFromSQL(excelfile29)
# a30 = dataFrameFromSQL(excelfile30)
# a31 = dataFrameFromSQL(excelfile31)
# a32 = dataFrameFromSQL(excelfile32)
# a33 = dataFrameFromSQL(excelfile33)



a01.to_sql('RAtesttest', engine, index=False)
# a02.to_sql('RA', engine, index=False, if_exists='append')
# a03.to_sql('RA', engine, index=False, if_exists='append')
# a04.to_sql('RA', engine, index=False, if_exists='append')
# a05.to_sql('RA', engine, index=False, if_exists='append')
# a06.to_sql('RA', engine, index=False, if_exists='append')
# a07.to_sql('RA', engine, index=False, if_exists='append')
# a08.to_sql('RA', engine, index=False, if_exists='append')
# a09.to_sql('RA', engine, index=False, if_exists='append')
# a10.to_sql('RA', engine, index=False, if_exists='append')
# a11.to_sql('RA', engine, index=False, if_exists='append')
# a12.to_sql('RA', engine, index=False, if_exists='append')
# a13.to_sql('RA', engine, index=False, if_exists='append')
# a14.to_sql('RA', engine, index=False, if_exists='append')
# a15.to_sql('RA', engine, index=False, if_exists='append')
# a16.to_sql('RA', engine, index=False, if_exists='append')
# a17.to_sql('RA', engine, index=False, if_exists='append')
# a18.to_sql('RA', engine, index=False, if_exists='append')
# a19.to_sql('RA', engine, index=False, if_exists='append')
# a20.to_sql('RA', engine, index=False, if_exists='append')
# a21.to_sql('RA', engine, index=False, if_exists='append')
# a22.to_sql('RA', engine, index=False, if_exists='append')
# a23.to_sql('RA', engine, index=False, if_exists='append')
# a24.to_sql('RA', engine, index=False, if_exists='append')
# a25.to_sql('RA', engine, index=False, if_exists='append')
# a26.to_sql('RA', engine, index=False, if_exists='append')
# a27.to_sql('RA', engine, index=False, if_exists='append')
# a28.to_sql('RA', engine, index=False, if_exists='append')
# a29.to_sql('RA', engine, index=False, if_exists='append')
# a30.to_sql('RA', engine, index=False, if_exists='append')
# a31.to_sql('RA', engine, index=False, if_exists='append')
# a32.to_sql('RA', engine, index=False, if_exists='append')
# a33.to_sql('RA', engine, index=False, if_exists='append')
#
#






