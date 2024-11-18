from sqlalchemy import text,create_engine
import os

username='Balli'
server = 'localhost'
driver ='ODBC+Driver+17+for+SQL+Server'
password=''
database = 'master'
connection_strings=f'mssql+pyodbc://{username}@{server}/{database}?Trusted_connection=Yes&driver={driver}'
engine=create_engine(connection_strings, isolation_level='AUTOCOMMIT')
with engine.connect() as conn:
    try:
        test = conn.execute(text("select name from master.sys.databases where name ='TestDB'"))
        if test.fetchone():
            print('database name already exist')
        else:
            conn.execute(text('create database TestDB '))
            print('database created successfully')
    except Exception as error:
        print(f'could not establish connection{error}')








