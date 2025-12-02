import mysql.connector
# Connect to MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='P@ssw0rd',
        database='northwind',
        port='3307'
    )
    
    if connection.is_connected():
        print("Connected to MySQL database")
            # Create cursor
        cursor = connection.cursor()
        
        # Execute query
        cursor.execute("SELECT * FROM category")
        
        # Fetch results
        results = cursor.fetchall()
        
        for row in results:
            print(row)

    else:
        print("Database not Connected")
except mysql.connector.Error as e:
    print(f"Error: {e}")
