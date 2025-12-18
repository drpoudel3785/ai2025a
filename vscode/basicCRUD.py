import mysql.connector

# 1. Connect
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="P@ssw0rd",
    database="TEST_DB1",
    port=3307
)
cursor = db.cursor()

# 2. Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT
)
""")

# 3. Insert
cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", ("Sita", 22))
cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", ("Ram", 22))
cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", ("Manish", 22))
cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", ("Gopal", 22))
db.commit()

# 4. Read
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

# 5. Update
cursor.execute("UPDATE students SET age=%s WHERE name=%s", (23, "Sita"))
db.commit()

# 6. Delete
# cursor.execute("DELETE FROM students WHERE name=%s", ("Sita",))
# db.commit()

# Close
cursor.close()
db.close()
