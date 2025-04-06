import mysql.connector

def show_mysql_tables():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host="localhost",
            user="root",           # 🔁 Change this if needed
            password="123Joel...",           # 🔁 Your MySQL password
            database="recipe_manager"  # 🔁 The database you want to inspect
        )

        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")

        tables = cursor.fetchall()

        if tables:
            print("Tables in the database:")
            for table in tables:
                print(f" - {table[0]}")
        else:
            print("No tables found in the database.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Run it
show_mysql_tables()