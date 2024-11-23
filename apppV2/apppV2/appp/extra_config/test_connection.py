import pyodbc

# Database connection parameters
server = 'DESKTOP-BIKQPHC'  # Your SQL Server instance name
database = 'LaptopDB'  # Your database name

# Create a connection string for Windows Authentication
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

try:
    # Establish a connection to the database
    with pyodbc.connect(conn_str) as conn:
        print("Connection successful!")

except pyodbc.Error as e:
    print("Error connecting to the database:", e)
