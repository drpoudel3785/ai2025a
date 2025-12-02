import mysql.connector, dbfunc
from mysql.connector import Error, errorcode

conn = dbfunc.getConnection()   #connection to DB
DB_NAME = 'TEST_DB'             #DB Name
TABLES = {}

TABLES['TUTOR'] = 'CREATE TABLE TUTOR (\
  Tut_Id VARCHAR(10) NOT NULL, \
  TName VARCHAR(45) NOT NULL, \
  DoB DATE NOT NULL, \
  HOURS DOUBLE, \
  PRIMARY KEY (Tut_Id));'

TABLES['STUDENT'] = 'CREATE TABLE STUDENT (\
SID VARCHAR(10) NOT NULL, \
PRIMARY KEY (SID), \
SNAME VARCHAR(30), \
EMAIL VARCHAR(30), \
Tutor_Id VARCHAR (10) NULL, \
FOREIGN KEY (Tutor_Id) \
  REFERENCES TUTOR (Tut_Id) \
  ON DELETE SET NULL \
  ON UPDATE CASCADE \
);'

TABLES['MODULES'] = 'CREATE TABLE MODULES(\
MID VARCHAR(15) NOT NULL, \
PRIMARY KEY (MID), \
MNAME VARCHAR(40), \
LEVEL VARCHAR(2), \
TUTOR_Tut_Id VARCHAR(10), \
FOREIGN KEY(TUTOR_Tut_Id) REFERENCES TUTOR (Tut_Id)  \
  ON UPDATE CASCADE \
    ON DELETE SET NULL );'

TABLES['STUDENT_ENROLEMENT'] = 'CREATE TABLE STUDENT_ENROLEMENT (\
SID VARCHAR(10) NOT NULL, \
FOREIGN KEY (SID) REFERENCES STUDENT(SID),\
MID VARCHAR(15) NOT NULL, \
FOREIGN KEY (MID) REFERENCES MODULES(MID),\
ACAD_YEAR VARCHAR(10),\
PRIMARY KEY (SID, MID, ACAD_YEAR));'

TABLES['TOPICS'] = 'CREATE TABLE TOPICS (\
  TId INT NOT NULL,\
  Tdesc VARCHAR(100) NULL,\
  Mod_Id VARCHAR(15) NULL,\
  PRIMARY KEY (TId),\
  CONSTRAINT MID\
    FOREIGN KEY (Mod_Id) REFERENCES MODULES (MID)\
    ON DELETE CASCADE\
    ON UPDATE CASCADE );'

TABLES['LEARN_PREFERENCE'] = 'CREATE TABLE LEARN_PREFERENCE (\
  TPreference VARCHAR(50) NULL,\
  APreference VARCHAR(50) NULL,\
  Stud_Id VARCHAR(10) NULL,  \
  CONSTRAINT SID\
    FOREIGN KEY (Stud_Id) REFERENCES STUDENT (SID)\
    ON DELETE CASCADE\
    ON UPDATE CASCADE );'

if conn != None:    #Checking if connection is None
    if conn.is_connected(): #Checking if connection is established
        print('MySQL Connection is established')                          
        dbcursor = conn.cursor()    #Creating cursor object
        dbcursor.execute('USE {};'.format(DB_NAME)) #use database    

        for table_name in TABLES:   #loop through TABLES 
            table_description = TABLES[table_name]
            try:
                print('Creating table {}:'.format(table_name), end='')
                dbcursor.execute(table_description)
            except mysql.connector.Error as e:
                if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('Table {} already exists.'.format(table_name))
                else:
                    print(e.msg)
            else:
                print('Table {} successfully created.'.format(table_name))       
        
        dbcursor.close()       
        conn.close() #Connection must be closed
    else:
        print('DB connection error')
else:
    print('DBFunc error')
