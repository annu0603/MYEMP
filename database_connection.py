import mysql.connector

def db_connect():
    try:
        # Connect to MySQL database
        db = mysql.connector.connect(
            host="myemp.c78wucmgyqix.ap-south-1.rds.amazonaws.com",
            user="myemp",
            passwd="passwordemp",
            database="employee_management"
        )
        
        if db.is_connected():
            print("Connected to MySQL database")
        
        return db
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None
