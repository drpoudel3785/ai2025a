#menu driven CRUD operations
import mysql.connector

# -------------------------------
# 1. DATABASE CONNECTION
# -------------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="P@ssw0rd",
    database="TEST_DB1",
    port=3307
)
cur = db.cursor()

# -------------------------------
# 2. FUNCTIONS
# -------------------------------

def add_student():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    
    sql = "INSERT INTO students (name, age) VALUES (%s, %s)"
    val = (name, age)
    cur.execute(sql, val)
    db.commit()
    print("Student added successfully!\n")
def show_students():
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    print("\n--- Student List ---")
    if not rows:
        print("No records found.\n")
        return
    for r in rows:
        print(f"ID: {r[0]} | Name: {r[1]} | Age: {r[2]}")
    print()
def edit_student():
    sid = int(input("Enter student ID to edit: "))
    new_name = input("Enter new name: ")
    new_age = int(input("Enter new age: "))
    sql = "UPDATE students SET name=%s, age=%s WHERE id=%s"
    val = (new_name, new_age, sid)
    cur.execute(sql, val)
    db.commit()
    if cur.rowcount == 0:
        print("No record found with that ID.\n")
    else:
        print("Record updated successfully!\n")
def delete_student():
    sid = int(input("Enter student ID to delete: "))
    sql = "DELETE FROM students WHERE id=%s"
    cur.execute(sql, (sid,))
    db.commit()
    if cur.rowcount == 0:
        print("No record found.\n")
    else:
        print("Record deleted successfully!\n")
# ------------------------------
# 3. MENU LOOP
# -------------------------------
def menu():
    while True:
        print("==== Student Management System ====")
        print("1. Add Student")
        print("2. Show Students")
        print("3. Edit Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            show_students()
        elif choice == "3":
            edit_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option! Try again.\n")


# Run Menu
menu()

# Close connection at the end
cur.close()
db.close()
