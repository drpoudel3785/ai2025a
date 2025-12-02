import mysql.connector, dbfunc, sys
from mysql.connector import Error, errorcode
 
""" Connect to MySQL database """
conn = dbfunc.getConnection()

DB_NAME = 'TEMP_DB'
TABLE_NAME = 'TEMP_TABLE' 
#You may create a dictionary where key can be table name 
# and value can be SQL statement. This will allow you to 
# run multiple create table statements in a loop
DBStatement = 'CREATE DATABASE ' + DB_NAME + ';'

TABLE_DESCRIPTION = 'CREATE TABLE ' + TABLE_NAME + ' ( \
    tempId VARCHAR(20)  NOT NULL, \
    Name VARCHAR(40) NOT NULL, \
    ADDRESS VARCHAR(100), \
    PRIMARY KEY (tempId));'
   
def create_database(dbcursor, DBNAME, DBStatement):
    try:
        dbcursor.execute(DBStatement)
    except mysql.connector.Error as e:
        print('Failed creating Database ', DBNAME)
        print(e)
        exit(1)

if conn != None:
    if conn.is_connected():
        print('MySQL Connection is established')
        # Write your DB queries here...                    
        dbcursor = conn.cursor()

        #CREATE database - only if you want to create new DB and 
        #your useraccount has privileges to create new Database
        #create_database(dbcursor, DB_NAME, DBStatement)
        
        try:
            dbcursor.execute('USE {}'.format(DB_NAME))
        except mysql.connector.Error as e:
            print('Database {} does not exists. '.format(DB_NAME))
            if e.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(dbcursor, DB_NAME, DBStatement)
                print("Database {} created successfully.".format(DB_NAME))
                conn.database = DB_NAME
                dbcursor.execute('USE {}'.format(conn.database))
                dbcursor.execute(TABLE_DESCRIPTION)
                print("Table {} created successfully.".format(TABLE_NAME))
                dbcursor.close()
            else:
                print(e)
                exit(1)
        
        conn.close() #Connection must be closed
    else:
        print('DB connection error')
else:
    print('DBFunc error')
