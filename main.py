from flask import Flask, render_template, request, redirect, url_for, flash
import os
import re
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Float, Integer, String, MetaData
from sqlalchemy.sql import select, insert, text
import datetime
from datetime import timedelta
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import time

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'xls'}

# Database
hostname = "localhost"
dbname = "db"
uname = "root"
pwd = "testtest"

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(host=hostname, db=dbname, user=uname, pw=pwd))
metadata = MetaData(engine)

today = datetime.datetime.today()

metadata.create_all(engine)
connection = engine.connect()

PZtemp = Table('PZdocsTemp', metadata,
              Column('ID', Integer),
              Column('Nazwa', String),
              Column('Jednostka', String),
              Column('Ilosc', Float),
              Column('Cena', Float)
           )

RWtemp = Table('RWdocsTemp', metadata,
           Column('ID', Integer),
           Column('Nazwa', String),
           Column('Ilosc', Float),
           Column('Jednostka', String)
           )

RAtemp = Table('RAdocsTemp', metadata,
           Column('Nazwa', String),
           Column('Ilosc', Float),
           Column('Netto', Float)
           )

BO = Table('BO', metadata,
           Column('ID', Integer, primary_key=True),
           Column('Nazwa', String),
           Column('Ilosc', Float),
           Column('Jednostka', String),
           Column('WartoscNetto', Float),
           Column('CenaZakupu', Float)
           )


def getAssortmentFromID(a):
    i = text(
        "SELECT * "
        "FROM asortyment "
        "WHERE idasortymentu LIKE :y"
    )
    result = connection.execute(i, {"y": a}).fetchall()
    return result


def getAssortmentByName(a):
    i = text(
        "SELECT * "
        "FROM asortyment "
        "WHERE Nazwa LIKE :y"
    )
    result = connection.execute(i, {"y": a}).fetchall()
    return result


def getSetByID(a):
    i = text(
        "SELECT * "
        "FROM komplety "
        "WHERE idkompletu LIKE :y"
    )
    result = connection.execute(i, {"y": a}).fetchall()
    return result


def getStockByName(a):
    i = text(
        "SELECT * "
        "FROM BO "
        "WHERE Nazwa LIKE :y"
    )
    result = connection.execute(i, {"y": a}).fetchall()
    return result


def updateBO(name, totalQuantity):
    update_statement = BO.update() \
        .where(BO.c.Nazwa == name) \
        .values(Ilosc=BO.c.Ilosc - totalQuantity,
                WartoscNetto=BO.c.Ilosc * BO.c.CenaZakupu)
    connection.execute(update_statement)


def selectFrom(table):
    s = select([table])
    result = connection.execute(s)
    a = list(result)
    return a


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    a = text(
        "CREATE TABLE IF NOT EXISTS db.PZdocs "
        "(ID BIGINT NOT NULL, "
        "Nazwa TEXT NOT NULL, "
        "Dokument TEXT NULL, "
        "Jednostka TEXT NULL, "
        "Ilosc DOUBLE NULL, "
        "Cena DOUBLE NULL, "
        "Data TEXT NULL)"
        "ENGINE=InnoDB "
        "DEFAULT CHARSET=utf8mb4 "
        "COLLATE=utf8mb4_general_ci; "
    )

    connection.execute(a)

    a = text(
        "CREATE TABLE IF NOT EXISTS db.RAdocs "
        "(ID BIGINT NOT NULL, "
        "Nazwa TEXT NOT NULL, "
        "Dokument TEXT NULL, "
        "Ilosc TEXT NULL, "
        "Netto DOUBLE NULL, "
        "VAT DOUBLE NULL, "
        "Brutto TEXT NULL, "
        "Stawka TEXT NULL, "
        "od TEXT NULL, "
        "do TEXT NULL)"
        "ENGINE=InnoDB "
        "DEFAULT CHARSET=utf8mb4 "
        "COLLATE=utf8mb4_general_ci; "
    )

    connection.execute(a)

    a = text(
        "CREATE TABLE IF NOT EXISTS db.RWdocs "
        "(ID BIGINT NOT NULL, "
        "Nazwa TEXT NOT NULL, "
        "Dokument TEXT NULL, "
        "Jednostka TEXT NULL, "
        "Ilosc DOUBLE NULL, "
        "Data TEXT NULL)"
        "ENGINE=InnoDB "
        "DEFAULT CHARSET=utf8mb4 "
        "COLLATE=utf8mb4_general_ci; "
    )

    connection.execute(a)

    a = text(
        "CREATE TABLE IF NOT EXISTS db.ZWdocs "
        "(ID BIGINT NOT NULL, "
        "Nazwa TEXT NOT NULL, "
        "Dokument TEXT NULL, "
        "Jednostka TEXT NULL, "
        "Ilosc DOUBLE NULL, "
        "Data TEXT NULL)"
        "ENGINE=InnoDB "
        "DEFAULT CHARSET=utf8mb4 "
        "COLLATE=utf8mb4_general_ci; "
    )

    connection.execute(a)

    a = text(
        "CREATE TABLE IF NOT EXISTS db.ZDdocs "
        "(ID BIGINT NOT NULL, "
        "Nazwa TEXT NOT NULL, "
        "Dokument TEXT NULL, "
        "Jednostka TEXT NULL, "
        "Ilosc DOUBLE NULL, "
        "Data TEXT NULL)"
        "ENGINE=InnoDB "
        "DEFAULT CHARSET=utf8mb4 "
        "COLLATE=utf8mb4_general_ci; "
    )

    connection.execute(a)

    # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


@app.route('/sm')
def presentSM():
    a = text(
        "SELECT * FROM BO"
    )
    data = connection.execute(a).fetchall()

    a = text(
        "SELECT UPDATE_TIME "
        "FROM   information_schema.tables "
        "WHERE  TABLE_SCHEMA = 'db' "
        "AND TABLE_NAME = 'BO'; "
    )

    # lastSMupdate = connection.execute(a).fetchall()
    lastSMupdate = [a[0] for a in connection.execute(a)]

    a = text(
        "SELECT UPDATE_TIME "
        "FROM   information_schema.tables "
        "WHERE  TABLE_SCHEMA = 'db' "
        "AND TABLE_NAME = 'PZdocs'; "
    )

    lastPZupdate = [a[0] for a in connection.execute(a)]

    a = text(
        "SELECT UPDATE_TIME "
        "FROM   information_schema.tables "
        "WHERE  TABLE_SCHEMA = 'db' "
        "AND TABLE_NAME = 'RWdocs'; "
    )

    lastRWupdate = [a[0] for a in connection.execute(a)]

    a = text(
        "SELECT UPDATE_TIME "
        "FROM   information_schema.tables "
        "WHERE  TABLE_SCHEMA = 'db' "
        "AND TABLE_NAME = 'RAdocs'; "
    )

    lastRAupdate = [a[0] for a in connection.execute(a)]

    a = text(
        "SELECT UPDATE_TIME "
        "FROM   information_schema.tables "
        "WHERE  TABLE_SCHEMA = 'db' "
        "AND TABLE_NAME = 'ZDdocs'; "
    )

    lastZDupdate = [a[0] for a in connection.execute(a)]

    a = text(
        "SELECT UPDATE_TIME "
        "FROM   information_schema.tables "
        "WHERE  TABLE_SCHEMA = 'db' "
        "AND TABLE_NAME = 'ZWdocs'; "
    )

    lastZWupdate = [a[0] for a in connection.execute(a)]

    if not lastSMupdate:  #Porównanie daty ostatniej aktualizacji tabeli do określenia rodzaju dokumentu
        return render_template('stockDocuments.html', data=data, lastSMupdate="Brak modyfikacji bilansu otwarcia")
    else:
        if lastPZupdate:
            if lastPZupdate[0] == lastSMupdate[0]:
                a = text(
                    "SELECT Dokument FROM PZdocs "
                    "ORDER BY Data DESC, Dokument DESC;"
                )
                lastDoc = connection.execute(a).fetchall()
                lastPZ = [a[0] for a in lastDoc]
                return render_template('stockDocuments.html', data=data, lastSMupdate=lastPZ[0])
        if lastRWupdate:
            if lastRWupdate[0] == lastSMupdate[0]:
                return render_template('stockDocuments.html', data=data, lastSMupdate="Ostatni przesłany dokument: RW")
        if lastZWupdate:
            if lastZWupdate[0] == lastSMupdate[0]:
                return render_template('stockDocuments.html', data=data, lastSMupdate="Ostatni przesłany dokument: ZW")
        if lastZDupdate:
            if lastZDupdate[0] == lastSMupdate[0]:
                return render_template('stockDocuments.html', data=data, lastSMupdate="Ostatni przesłany dokument: ZD")
        if lastRAupdate:
            if lastRAupdate[0] == lastSMupdate[0]:
                return render_template('stockDocuments.html', data=data, lastSMupdate="Ostatni przesłany dokument: Raport sprzedaży")
        else:
            return render_template('stockDocuments.html', data=data, lastSMupdate="Ostatni przesłany dokument: Nieznany")

    # return render_template('stockDocuments.html', data=data, lastSMupdate="Btesttesttestotwarcia")
    # a =text(
    #     "SELECT UPDATE_TIME "
    #     "FROM   information_schema.tables "
    #     "WHERE  TABLE_SCHEMA = 'db' "
    #     "AND TABLE_NAME = BO "
    # )
    # lastUpdate = connection.execute(a).fetchall()
    # print(lastUpdate)


@app.route('/pz')
def presentPZ():
    a = text(
        "CREATE TABLE IF NOT EXISTS db.PZdocsTemp "
        "(ID BIGINT NOT NULL, "
        "Nazwa TEXT NOT NULL, "
        "Dokument TEXT NULL, "
        "Jednostka TEXT NULL, "
        "Ilosc DOUBLE NULL, "
        "Cena DOUBLE NULL, "
        "Data TEXT NULL)"
        "ENGINE=InnoDB "
        "DEFAULT CHARSET=utf8mb4 "
        "COLLATE=utf8mb4_general_ci; "
    )

    connection.execute(a)

    a = text(
        "SELECT * FROM PZdocs "
        "ORDER BY Data DESC, Dokument DESC;"
    )
    data = connection.execute(a).fetchall()

    a = text(
        "SELECT Dokument FROM PZdocs "
        "ORDER BY Data DESC, Dokument DESC;"
    )

    lastDoc = connection.execute(a).fetchall()
    if not lastDoc:
        return render_template('pzDocuments.html', data=data, lastPZ=0)
    else:
        lastPZ = [a[0] for a in lastDoc]
        return render_template('pzDocuments.html', data=data, lastPZ=lastPZ[0])

    # return render_template('pzDocuments.html', data=data, lastPZ=lastPZ[0])

    # a = text(
    #     "SELECT Dokument FROM PZdocs "
    #     "ORDER BY Data ASC, Dokument ASC;"
    # )
    #
    # docNumber = connection.execute(a).fetchall()
    #


    # count = 0
    #
    # #
    # numbers = []
    #
    # for a in docNumber:
    #     count+=1
    #     print(a[0])
    #
    #     docNumberFromSQL = re.split('[/](.*)', a[0])
    #     print(docNumberFromSQL[0])
    #     if count == docNumberFromSQL[0]:
    #         print("Elegancko mamy ten dokument:", docNumberFromSQL[0])
    #     else:
    #         print("Brakuje: ",count)
    #     numbers.append(docNumberFromSQL[0])
    # print(numbers)
    # for a in numbers:
    #     count+=1
    #     if count == a:
    #         print("Jest taki")
    #     else:
    #         print("Brakuje tego: ",a)
    #     #

        #     print("Elegancko mamy ten dokument:", docNumberFromSQL[0])
        #
        #     print("Brakuje: ",count, "/PZ/")
    # date = datetime.datetime.strptime(lastDocFromSql[0], '%Y-%m-%d')
    # goodFromDate = date + timedelta(days=1)
    # goodToDate = today - timedelta(days=1)
    # goodFromDate = str(goodFromDate.strftime('%Y-%m-%d'))
    # goodToDate = str(goodToDate.strftime('%Y-%m-%d'))
    # print('Wykonaj raport od: ', goodFromDate, ' do: ', goodToDate)


@app.route('/pz', methods=['POST'])
def uploadPZ():
    # get the uploaded file
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        if uploaded_file and allowed_file(uploaded_file.filename):
            uploaded_file.save(file_path)
            importPZ(file_path)

            if checkIfPZExist(importPZ(file_path)):

                flash(u'Dokument istnieje w bazie lub zły typ dokumentu', 'error')
                return redirect(url_for('presentPZ'))

            else:
                flash("Dokument został przesłany pomyślnie")
                return redirect(url_for('presentPZ'))
        else:
            flash(u'Chujowy typ pliku', 'error')
            return redirect(url_for('presentPZ'))
    else:
        flash(u'Brak dokumentu', 'error')
        return redirect(url_for('presentPZ'))


def importPZ(filePath):
    xlsData = pd.read_excel(filePath, skiprows=4, usecols=['Lp.', 'Nazwa', 'Jedn.', 'Ilość', 'Cena', 'Dokument', 'Data'])
    open(filePath, "r")
    xlsData.rename(columns={'Ilość': 'Ilosc'}, inplace=True)
    xlsData.dropna(subset=["Lp."], inplace=True)  # Jeśli kolumna Nazwa zawiera Nan -> wyjeboj
    xlsData = xlsData[xlsData['Lp.'].astype(str).str.isdigit()]
    xlsData['Ilosc'] = xlsData['Ilosc'].str.replace(' ', '')
    xlsData['Ilosc'] = xlsData['Ilosc'].str.replace(',', '.').astype(float)
    xlsData['Cena'] = xlsData['Cena'].str.replace(',', '.').astype(float)
    xlsData['Jedn.'] = xlsData['Jedn.'].str.replace('Szt.', 'Szt')
    xlsData.rename(columns={'Jedn.': 'Jednostka'}, inplace=True)
    xlsData.rename(columns={'Lp.': 'ID'}, inplace=True)
    xlsData['Dokument'] = xlsData['Dokument'].str.replace('( [(][0-9]*[/]*[0-9]*[)])', '')
    xlsData['Nazwa'] = xlsData['Nazwa'].str.replace('( [(][0-9]*[/]*[0-9]*[)])', '')
    return xlsData


def checkIfPZExist(df):
    ifExist = False
    for a in df['Dokument']:
        docHeader = re.split('([/][^0-9]*[/])', a)
        if docHeader[1] == '/PZ/':

            if ifExist:
                break
            else:
                i = text(
                "SELECT * "
                "FROM PZdocs "
                "WHERE Dokument LIKE :y"
                )
                result = connection.execute(i, {"y": a}).fetchall()

                if result:
                    ifExist = True
                    break
        else:
            ifExist = True
            break

    if not ifExist:
        addToPZdocsTemp(df)  # Dodanie raportu (dataframe) do tymczasowej tabeli
        PZtoStockCalculation()  # Dodanie towaru z PZ do stanu magazynowego
        addToPZdocs(df)  # Dodanie do tabeli z wszystkimi paragonami
        PZtemp.drop(engine)  # usuniecie tymczasowej tabeli potrzebnej do przeliczenia

    return ifExist


def addToPZdocsTemp(df):
    b = text(
        "SELECT COUNT(*) "
        "FROM PZdocsTemp;"
    )
    rowsCount = [a[0] for a in connection.execute(b)]
    count = 0
    for i, row in df.iterrows():
        count += 1
        sql = "INSERT INTO PZdocsTemp (ID, Nazwa, Dokument, Jednostka, Cena, Ilosc, Data) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        value = (
            rowsCount[0] + count, row['Nazwa'], row['Dokument'], row['Jednostka'], row['Cena'], row['Ilosc'],
            row['Data'])
        connection.execute(sql, value)


def PZtoStockCalculation():
    pz = selectFrom(PZtemp)

    for a in pz:

        if a[4] == 0:  # PZ z pozycją 0zł traktuję jako RW

            ifExist = False
            sm = selectFrom(BO)

            for b in sm:
                if a[1] == b[1]:
                    ifExist = True

                    update_statement = BO.update() \
                        .where(BO.c.ID == b[0]) \
                        .values(Ilosc=BO.c.Ilosc - a[3],
                                WartoscNetto=BO.c.WartoscNetto - (a[3] * BO.c.CenaZakupu)
                                )

                    connection.execute(update_statement)

            if not ifExist:  # jeśli nie istnieje asortyment na magazynie to dodaje pozycje
                sm = selectFrom(BO)

                i = insert(BO)
                i = i.values({'ID': len(sm) + 1, 'Nazwa': a[1], 'Ilosc': a[3],
                              'Jednostka': a[2], 'WartoscNetto': a[3] * a[4],
                              'CenaZakupu': a[4]})  # dodanie z pz asortymentu którego nie było na magazynie ID + 1
                connection.execute(i)

        else:
            ifExist = False
            sm = selectFrom(BO)

            for b in sm:
                if a[1] == b[1]:
                    ifExist = True

                    update_statement = BO.update() \
                        .where(BO.c.ID == b[0]) \
                        .values(Ilosc=BO.c.Ilosc + a[3],  # Dodanie ilości na magazyn z PZ
                                WartoscNetto=BO.c.WartoscNetto + (a[3] * a[4]),  # Zwiększenie wartości magazynu
                                CenaZakupu=((b[2] * b[5]) + (a[3] * a[4])) / (b[2] + a[3])
                                )

                    connection.execute(update_statement)

            if not ifExist:  # jeśli nie istnieje asortyment na magazynie to dodaje pozycje

                sm = selectFrom(BO)
                i = insert(BO)
                i = i.values({'ID': len(sm) + 1, 'Nazwa': a[1], 'Ilosc': a[3],
                              'Jednostka': a[2], 'WartoscNetto': a[3] * a[4],
                              'CenaZakupu': a[4]})  # dodanie z pz asortymentu którego nie było na magazynie ID + 1
                connection.execute(i)


def addToPZdocs(df):
    b = text(
        "SELECT COUNT(*) "
        "FROM PZdocs;"
    )
    rowsCount = [a[0] for a in connection.execute(b)]
    count = 0
    for i, row in df.iterrows():
        count += 1
        sql = "INSERT INTO PZdocs (ID, Nazwa, Dokument, Jednostka, Cena, Ilosc, Data) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        value = (
        rowsCount[0] + count, row['Nazwa'], row['Dokument'], row['Jednostka'], row['Cena'], row['Ilosc'], row['Data'])
        connection.execute(sql, value)


@app.route('/rw')
def presentRW():
    a = text(
        "CREATE TABLE IF NOT EXISTS db.RWdocsTemp "
        "(ID BIGINT NOT NULL, "
        "Nazwa TEXT NOT NULL, "
        "Dokument TEXT NULL, "
        "Jednostka TEXT NULL, "
        "Ilosc DOUBLE NULL, "
        "Data TEXT NULL)"
        "ENGINE=InnoDB "
        "DEFAULT CHARSET=utf8mb4 "
        "COLLATE=utf8mb4_general_ci; "
    )

    connection.execute(a)

    a = text (
        "SELECT * FROM RWdocs "
        "ORDER BY Data DESC, Dokument DESC;"
    )
    data = connection.execute(a).fetchall()
    return render_template('rwDocuments.html', data=data)


@app.route('/rw', methods=['POST'])
def uploadRW():
    # get the uploaded file
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        if uploaded_file and allowed_file(uploaded_file.filename):
            uploaded_file.save(file_path)
            importRW(file_path)

            if checkIfRWExist(importRW(file_path)):

                flash(u'Dokument istnieje w bazie lub zły typ dokumentu', 'error')
                return redirect(url_for('presentRW'))

            else:
                flash("Dokument został przesłany pomyślnie")
                return redirect(url_for('presentRW'))
        else:
            flash(u'Chujowy typ pliku', 'error')
            return redirect(url_for('presentRW'))
    else:
        flash(u'Brak dokumentu', 'error')
        return redirect(url_for('presentRW'))


def importRW(filePath):

    xlsData = pd.read_excel(filePath, skiprows=4, usecols=['Lp.', 'Nazwa', 'Jedn.', 'Ilość', 'Dokument', 'Data'])
    open(filePath, "r")
    xlsData.rename(columns={'Ilość': 'Ilosc'}, inplace=True)
    xlsData.dropna(subset=["Lp."], inplace=True)  # Jeśli kolumna Nazwa zawiera Nan -> wyjeboj
    xlsData = xlsData[xlsData['Lp.'].astype(str).str.isdigit()]
    xlsData['Ilosc'] = xlsData['Ilosc'].str.replace(' ', '')
    xlsData['Ilosc'] = xlsData['Ilosc'].str.replace(',', '.').astype(float)
    # xlsData['Cena'] = xlsData['Cena'].str.replace(',', '.').astype(float)
    xlsData['Jedn.'] = xlsData['Jedn.'].str.replace('Szt.', 'Szt')
    xlsData.rename(columns={'Jedn.': 'Jednostka'}, inplace=True)
    xlsData.rename(columns={'Lp.': 'ID'}, inplace=True)
    xlsData['Dokument'] = xlsData['Dokument'].str.replace('( [(][0-9]*[/]*[0-9]*[)])', '')
    xlsData['Nazwa'] = xlsData['Nazwa'].str.replace('( [(][0-9]*[/]*[0-9]*[)])', '')
    return xlsData

def checkIfRWExist(df):

    ifExist = False

    for a in df['Dokument']:
        docNumber = re.split('[/](.*)', a)
        docHeader = re.split('([/][^0-9]*[/])', a)
        if docHeader[1] == '/RW/':

            if ifExist:
                break
            else:
                i = text(
                "SELECT * "
                "FROM RWdocs "
                "WHERE Dokument LIKE :y"
                )
                result = connection.execute(i, {"y": a}).fetchall()
                result = [a[2] for a in result]
                print(result)
                for b in result:
                    docNumberFromDB = re.split('[/](.*)', b)
                    if docNumberFromDB[0] <= docNumber[0]:
                        ifExist = True
                        break
        else:
            ifExist = True
            break

    if not ifExist:
        addToRWdocsTemp(df)  # Dodanie raportu (dataframe) do tymczasowej tabeli
        RWtoStockCalculation()  # Dodanie towaru z RW do stanu magazynowego
        addToRWdocs(df)  # Dodanie do tabeli z wszystkimi dokumentami
        RWtemp.drop(engine)  # usuniecie tymczasowej tabeli potrzebnej do przeliczenia

    return ifExist


def addToRWdocsTemp(df):
    b = text(
        "SELECT COUNT(*) "
        "FROM RWdocsTemp;"
    )
    rowsCount = [a[0] for a in connection.execute(b)]
    count = 0
    for i, row in df.iterrows():
        count += 1
        sql = "INSERT INTO RWdocsTemp (ID, Nazwa, Dokument, Jednostka, Ilosc, Data) VALUES (%s, %s, %s, %s, %s, %s)"
        value = (
            rowsCount[0] + count, row['Nazwa'], row['Dokument'], row['Jednostka'], row['Ilosc'],
            row['Data'])
        connection.execute(sql, value)


def RWtoStockCalculation():

    rw = selectFrom(RWtemp)

    for a in rw:
        print(a)
        ifExist = False
        sm = selectFrom(BO)

        for b in sm:

            if a[1] == b[1]:
                ifExist = True

                update_statement = BO.update() \
                    .where(BO.c.ID == b[0]) \
                    .values(Ilosc=BO.c.Ilosc + a[2],
                            WartoscNetto=BO.c.WartoscNetto + (a[2] * b[5]))  # rw do stanu

                connection.execute(update_statement)

        if not ifExist:
            print("Brak pozycji ", a, " z dokumentu RW na stanie magazynu", file=open("output.txt", "a"))

def addToRWdocs(df):
    b = text(
        "SELECT COUNT(*) "
        "FROM RWdocs;"
    )
    rowsCount = [a[0] for a in connection.execute(b)]
    count = 0
    for i, row in df.iterrows():
        count += 1
        sql = "INSERT INTO RWdocs (ID, Nazwa, Dokument, Jednostka, Ilosc, Data) VALUES (%s, %s, %s, %s, %s, %s)"
        value = (
        rowsCount[0] + count, row['Nazwa'], row['Dokument'], row['Jednostka'], row['Ilosc'], row['Data'])
        connection.execute(sql, value)

# @app.route('/dashboard/')
# def display_deals():
#
#     try:
#         c, conn = connection()
#
#         query = "SELECT * from submissions"
#         c.execute(query)
#
#         data = c.fetchall()
#
#         conn.close()
#
#         return data
#
#         return render_template("dashboard.html", data=data)
#
#     except Exception as e:
#         return (str(e))


# Get the uploaded files
# @app.route("/", methods=['POST'])
# def uploadFiles():
#       # get the uploaded file
#       uploaded_file = request.files['file']
#       if uploaded_file.filename != '':
#            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
#           # set the file path
#            uploaded_file.save(file_path)
#           # save the file
#       return redirect(url_for('index'))


@app.route('/redirectSaleReport')
def getSaleReport():
    driver = webdriver.Chrome(executable_path="/Users/szymonbzdyk/Downloads/chromedriver")
    driver.get ("http://172.21.2.246:8087/eobiekt")
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/form/div/div[2]/div/div/div').click() #Otwarcie listy z uzytkownikami
    driver.find_element_by_xpath('//*[@id="menu-"]/div[3]/ul').send_keys('x' + Keys.RETURN) #Wybor uzytkownika z listy dostepnych
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/form/div/div[3]/div/div/input').send_keys('xxxxxx123' + Keys.RETURN) #Hasło
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="navbar"]/div/div[2]').click() #Menu Raporty
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[1]/div[3]/div/button[6]').click() #Zakładka RAPORTY VAT
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[3]/div[4]/a/div').click() #Otwarcie raportu sprzedaży wg asortymentu
    time.sleep(0.5)


@app.route('/redirectPZReport')
def getPZReport():
    driver = webdriver.Chrome(executable_path="/Users/szymonbzdyk/Downloads/chromedriver")
    driver.get("http://172.21.2.246:8087/eobiekt")
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div/form/div/div[2]/div/div/div').click()  # Otwarcie listy z uzytkownikami
    driver.find_element_by_xpath('//*[@id="menu-"]/div[3]/ul').send_keys(
        'x' + Keys.RETURN)  # Wybor uzytkownika z listy dostepnych
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/form/div/div[3]/div/div/input').send_keys(
        'xxxxxx123' + Keys.RETURN)  # Hasło
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="navbar"]/div/div[2]').click()  # Menu Raporty
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[1]/div[3]/div/button[7]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[3]/div[4]/a/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div[1]/div[11]/div/div/div[1]/div/div/label[1]/span[1]/span[1]/input').click()  # wybor typu dokumentu


@app.route('/redirectRWReport')
def getRWReport():
    driver = webdriver.Chrome(executable_path="/Users/szymonbzdyk/Downloads/chromedriver")
    driver.get("http://172.21.2.246:8087/eobiekt")
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div/form/div/div[2]/div/div/div').click()  # Otwarcie listy z uzytkownikami
    driver.find_element_by_xpath('//*[@id="menu-"]/div[3]/ul').send_keys(
        'x' + Keys.RETURN)  # Wybor uzytkownika z listy dostepnych
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/form/div/div[3]/div/div/input').send_keys(
        'xxxxxx123' + Keys.RETURN)  # Hasło
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="navbar"]/div/div[2]').click()  # Menu Raporty
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[1]/div[3]/div/button[7]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[3]/div[4]/a/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div[1]/div[11]/div/div/div[1]/div/div/label[3]/span[1]/span[1]/input').click()  # Wybor typu dokumentu


@app.route('/redirectZWReport')
def getZWReport():
    driver = webdriver.Chrome(executable_path="/Users/szymonbzdyk/Downloads/chromedriver")
    driver.get("http://172.21.2.246:8087/eobiekt")
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div/form/div/div[2]/div/div/div').click()  # Otwarcie listy z uzytkownikami
    driver.find_element_by_xpath('//*[@id="menu-"]/div[3]/ul').send_keys(
        'x' + Keys.RETURN)  # Wybor uzytkownika z listy dostepnych
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/form/div/div[3]/div/div/input').send_keys(
        'xxxxxx123' + Keys.RETURN)  # Hasło
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="navbar"]/div/div[2]').click()  # Menu Raporty
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[1]/div[3]/div/button[7]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[3]/div[4]/a/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div[1]/div[11]/div/div/div[1]/div/div/label[5]/span[1]/span[1]/input').click()  # Wybor typu dokumentu


@app.route('/redirectZDReport')
def getZDReport():
    driver = webdriver.Chrome(executable_path="/Users/szymonbzdyk/Downloads/chromedriver")
    driver.get("http://172.21.2.246:8087/eobiekt")
    driver.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div/form/div/div[2]/div/div/div').click()  # Otwarcie listy z uzytkownikami
    driver.find_element_by_xpath('//*[@id="menu-"]/div[3]/ul').send_keys(
        'x' + Keys.RETURN)  # Wybor uzytkownika z listy dostepnych
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/form/div/div[3]/div/div/input').send_keys(
        'xxxxxx123' + Keys.RETURN)  # Hasło
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="navbar"]/div/div[2]').click()  # Menu Raporty
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[1]/div[3]/div/button[7]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[3]/div[4]/a/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[1]/div[11]/div/div/div[1]/div/div/label[7]/span[1]/span[1]/input').click() #Wybor typu dokumentu


@app.route('/addBills')
def presentRA():
    a = text(
        "CREATE TABLE IF NOT EXISTS db.RAdocsTemp "
        "(ID BIGINT NOT NULL, "
        "Nazwa TEXT NOT NULL, "
        "Dokument TEXT NULL, "
        "Ilosc TEXT NULL, "
        "Netto DOUBLE NULL, "
        "VAT DOUBLE NULL, "
        "Brutto TEXT NULL, "
        "Stawka TEXT NULL, "
        "od TEXT NULL, "
        "do TEXT NULL)"
        "ENGINE=InnoDB "
        "DEFAULT CHARSET=utf8mb4 "
        "COLLATE=utf8mb4_general_ci; "
    )

    connection.execute(a)

    a = text (
        "SELECT * FROM RAdocs "
        "ORDER BY Dokument DESC LIMIT 30;"
    )
    data = connection.execute(a).fetchall()
    a = text(
        "SELECT MAX(do) FROM RAdocs "
        "ORDER BY do DESC;"
    )
    validDate = connection.execute(a).fetchall()
    dataFromSql = [a[0] for a in validDate]
    if not dataFromSql[0]:
        return render_template('addBills.html', data=data, dateFrom=today, dateTo=today)
    else:
        date = datetime.datetime.strptime(dataFromSql[0], '%Y-%m-%d')
        goodFromDate = date + timedelta(days=1)
        goodToDate = today - timedelta(days=1)
        goodFromDate = str(goodFromDate.strftime('%Y-%m-%d'))
        goodToDate = str(goodToDate.strftime('%Y-%m-%d'))## proponowana data raportu

        return render_template('addBills.html', data=data, dateFrom=goodFromDate, dateTo=goodToDate)


@app.route('/addBills', methods=['POST'])
def uploadRA():
    # get the uploaded file
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        if uploaded_file and allowed_file(uploaded_file.filename):
            uploaded_file.save(file_path)
            importRA(file_path)

            if checkIfRAExist(importRA(file_path)):

                flash(u'Dokument istnieje w bazie lub zły typ dokumentu', 'error')
                return redirect(url_for('presentRA'))

            else:
                flash("Dokument został przesłany pomyślnie")
                return redirect(url_for('presentRA'))
        else:
            flash(u'Chujowy typ pliku', 'error')
            return redirect(url_for('presentRA'))

    else:
        flash(u'Brak dokumentu', 'error')
        return redirect(url_for('presentRA'))


def importRA(filepath):
    xlsData = pd.read_excel(filepath, usecols=['Chochołowskie Termy Sp. z o. o.'])
    xlsData.dropna(subset=["Chochołowskie Termy Sp. z o. o."], inplace=True)
    getDate = xlsData['Chochołowskie Termy Sp. z o. o.']

    for a in getDate:
        okDate = re.findall('([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])', a)
        if okDate:
            fromDate = okDate[0]
            toDate = okDate[1]

    xlsData = pd.read_excel(filepath, skiprows=4)
    xlsData = xlsData.drop(['Nazwa asortymentu'], axis=1)
    xlsData = xlsData.drop(['Ilość'], axis=1)
    xlsData = xlsData.drop(['Unnamed: 0'], axis=1)  # drop columny
    xlsData = xlsData.drop(['Unnamed: 2'], axis=1)
    xlsData = xlsData.drop(['Unnamed: 3'], axis=1)
    xlsData = xlsData.drop(['Unnamed: 6'], axis=1)

    xlsData.rename(columns={'Unnamed: 9': 'od'}, inplace=True)
    xlsData.rename(columns={'Unnamed: 10': 'do'}, inplace=True)

    xlsData['od'] = fromDate
    xlsData['do'] = toDate

    xlsData = xlsData.drop(['Unnamed: 11'], axis=1)
    xlsData = xlsData.drop(['Unnamed: 13'], axis=1)
    xlsData = xlsData.drop(['Unnamed: 15'], axis=1)
    xlsData = xlsData.drop(['Unnamed: 17'], axis=1)
    xlsData = xlsData.drop(['Unnamed: 18'], axis=1)

    xlsData.rename(columns={'Unnamed: 5': 'Nazwa'}, inplace=True)
    xlsData.rename(columns={'Unnamed: 8': 'Ilosc'}, inplace=True)

    xlsData.dropna(subset=["Ilosc"], inplace=True)  # Jeśli kolumna Nazwa zawiera Nan -> wyjeboj

    xlsData['Ilosc'] = xlsData['Ilosc'].str.replace(' ', '')

    xlsData['Ilosc'] = xlsData['Ilosc'].str.replace(',', '.').astype(float)
    xlsData['Netto'] = xlsData['Netto'].str.replace(' ', '')
    xlsData['Netto'] = xlsData['Netto'].str.replace(',', '.').astype(float)
    xlsData['Brutto'] = xlsData['Brutto'].str.replace(' ', '')
    xlsData['Brutto'] = xlsData['Brutto'].str.replace(',', '.').astype(float)
    xlsData['VAT'] = xlsData['VAT'].str.replace(' ', '')
    xlsData['VAT'] = xlsData['VAT'].str.replace(',', '.').astype(float)
    xlsData['Dokument'] = xlsData['Dokument'].str.replace('( [(][0-9]*[/]*[0-9]*[)])', '')

    return xlsData


def checkIfRAExist(df):

    ifExist = False

    for a in df['Dokument']:
        # docNumber = re.split('[/](.*)', a)
        docHeader = re.split('([/][^0-9]*[/])', a)
        if docHeader[1] == '/RA/':

            if ifExist:
                break
            else:
                i = text(
                "SELECT * "
                "FROM RAdocs "
                "WHERE Dokument LIKE :y"
                )
                result = connection.execute(i, {"y": a}).fetchall()

                if result:
                    ifExist = True
                    break
        else:
            ifExist = True
            break

    if not ifExist:

        addToRAdocsTemp(df) #Dodanie raportu (dataframe) do tymczasowej tabeli
        stockCalculation() #Przeliczenie magazynu
        addToRAdocs(df) #Dodanie do tabeli z wszystkimi paragonami
        RAtemp.drop(engine) #usuniecie tymczasowej tabeli potrzebnej do przeliczenia

    return ifExist


def addToRAdocsTemp(df):
    b = text(
        "SELECT COUNT(*) "
        "FROM RAdocsTemp;"
    )

    rowsCount = [a[0] for a in connection.execute(b)]
    count = 0
    for i, row in df.iterrows():
        count += 1
        sql = "INSERT INTO RAdocsTemp (ID, Nazwa, Dokument, Ilosc, Netto, VAT, Brutto, Stawka, od, do) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        value = (
        rowsCount[0] + count, row['Nazwa'], row['Dokument'], row['Ilosc'], row['Netto'], row['VAT'], row['Brutto'],
        row['Stawka'], row['od'], row['do'])
        connection.execute(sql, value)


def addToRAdocs(df):
    b = text(
        "SELECT COUNT(*) "
        "FROM RAdocs;"
    )

    rowsCount = [a[0] for a in connection.execute(b)]
    count = 0
    for i, row in df.iterrows():
        count += 1
        sql = "INSERT INTO RAdocs (ID, Nazwa, Dokument, Ilosc, Netto, VAT, Brutto, Stawka, od, do) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        value = (
        rowsCount[0] + count, row['Nazwa'], row['Dokument'], row['Ilosc'], row['Netto'], row['VAT'], row['Brutto'],
        row['Stawka'], row['od'], row['do'])
        connection.execute(sql, value)


def stockCalculation():
    # count = 0
    # allRA = len(ra)
    ra = selectFrom(RAtemp)
    for a in ra:
        #
        # count += 1
        # progressValue(count, allRA)
        print("Pozycja na paragonie ", a[0], " sprzedany ", a[1], "x za cenę: ", a[2], " zł")

        assortmentID = [b[0] for b in getAssortmentByName(a[0])]
        quantitySet = [b[4] for b in getAssortmentByName(a[0])]

        if not assortmentID:
            print("Asortyment nie do ściągnięcia ", a[0])

        else:
            set = [a for a in getSetByID(assortmentID[0])]

            for f in set:

                assortmentIDFromSet = [q[0] for q in getAssortmentFromID(f[1])]
                assortmentNameFromSet = [q[1] for q in getAssortmentFromID(f[1])]
                assortmentQuantityFromSet = [q[4] for q in getAssortmentFromID(f[1])]

                total = (f[0] / quantitySet[0]) * a[1]

                surowiec = [e[1] for e in getStockByName(assortmentNameFromSet[0])]

                if not surowiec:  # Brak surowca do ściągnięcia z magazynu (receptura w recepturze)

                    setInSet = [a for a in getSetByID(assortmentIDFromSet[0])]

                    for l in setInSet:
                        assortmentIDFromSetInSet = [a[0] for a in getAssortmentFromID(l[1])]
                        assortmentNameFromSetInSet = [a[1] for a in getAssortmentFromID(l[1])]
                        total = (((l[0] / assortmentQuantityFromSet[0]) * f[0]) / quantitySet[0]) * a[1]
                        print("Sciagam ", assortmentNameFromSetInSet[0], " w ilości ", total)
                        updateBO(assortmentNameFromSetInSet[0], total)

                else:  # Surowiec do ściągnięcia z magazynu
                    print("Sciągam ", assortmentNameFromSet[0], " w ilości ", total)
                    updateBO(assortmentNameFromSet[0], total)


@app.route('/assortment')
def presentAssortment():
    return render_template('assortment.html')


@app.route('/sets')
def presentSets():
    return render_template('sets.html')


@app.route('/inventory')
def presentInventory():
    return render_template('inventory.html')


if __name__ == "__main__":
    app.secret_key = 'tajne'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5000)
