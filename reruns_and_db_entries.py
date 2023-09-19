import pyodbc
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select,URL

#run parameters
number_of_runs=100
counter=1

#connect to DB
server = 'LAPTOP-SLDJ2N3Q\SQLEXPRESS'
mydatabase = 'Critical Illness insurance'
#username = 'your_username'
#password = 'your_password'

ALCHEMY_URL = URL.create(
"mssql+pyodbc",
host=server,
database=mydatabase,
query={
    "driver": "ODBC Driver 17 for SQL Server",
},)

# Create an engine and a connection object
engine=create_engine((ALCHEMY_URL))
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database+';Trusted_Connection=yes;')
cnxn=engine.connect()
connection=engine.raw_connection()
runcon=connection.cursor()

while counter<=number_of_runs:
    # Create a sample DataFrame
    df = pd.DataFrame({
        'index': ["SU", "MU", "R"],
        'col1': ['value1', 'value2', 'value3'],
        'col2': [1, 2, 3],
        'col3': [1.1, 2.2, 3.3]
    })

    df.set_index('index', inplace=True)

    # Convert the DataFrame to a format that can be written to SQL Server
    table_name = 'test'
    df.to_sql(table_name, engine, if_exists='append', index=True, index_label='index')
    sql = 'update ' + table_name+' set run= (?) WHERE run IS NULL'
    runcon.execute(sql,counter)
    runcon.commit()
    counter+=1

runcon.close()
pass