import mysql.connector, dbfunc
conn = dbfunc.getConnection()   #connection to DB
DB_NAME = 'TEST_DB1'             #DB Name
TABLE_NAME = 'TEST_TABLE'

TABLE_DESCRIPTION = 'CREATE TABLE ' + TABLE_NAME + ' ( \
    tempId VARCHAR(20)  NOT NULL, \
    Name VARCHAR(40) NOT NULL, \
    ADDRESS VARCHAR(100), \
    PRIMARY KEY (tempId));'

if conn != None:    #Checking if connection is None
    if conn.is_connected(): #Checking if connection is established
        print('MySQL Connection is established')                          
        dbcursor = conn.cursor()    #Creating cursor object
        dbcursor.execute('USE {};'.format(DB_NAME)) #use database        
        dbcursor.execute(TABLE_DESCRIPTION) 
        print('Table {} created successfully.'.format(TABLE_NAME))               
        conn.close() #Connection must be closed
    else:
        print('DB connection error')
else:
    print('DBFunc error')
