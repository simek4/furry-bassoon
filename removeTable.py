from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select, update, insert, text


hostname = "localhost"
dbname = "db"
uname = "root"
pwd = "testtest"

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(host=hostname, db=dbname, user=uname, pw=pwd))
metadata = MetaData(engine)

metadata.create_all(engine)
connection = engine.connect()




def removeRAdocsTemp():

    a = text(
        "DROP TABLE IF EXISTS RAdocsTemp;"
    )
    connection.execute(a).fetchall()