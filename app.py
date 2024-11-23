# from app import create_app
# import pandas as pd

# # app = create_app()

# laptop_prices = pd.read_csv("database/laptop_prices.csv")
# print(laptop_prices)

# if __name__ == '__main__':
    # app.run(debug=True )  # Start the Flask application




import pyodbc
import pandas as pd

# Database connection parameters
server = 'DESKTOP-BIKQPHC'  # Your SQL Server instance name
database = 'LaptopDB'  # Your database name

# Create a connection string for Windows Authentication
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

try:
    # Establish a connection to the database
    with pyodbc.connect(conn_str) as conn:
        print("Connection successful!")
        
        # Define the SQL query to select the top 1000 rows from the ProductDetails table
        query = """
        SELECT TOP (1000) 
            [DetailID],[ProductID], [CPUModel],  [CPUFreq], [PrimaryStorage], [PrimaryStorageType],[SecondaryStorage],
            [SecondaryStorageType],[GPUCompany],[GPUModel],[OS],[Ram], [Inches],[ProdWeight],[Screen],[Price]
        FROM [LaptopDB].[dbo].[ProductDetails]
        """
                # Use pandas to execute the query and load the data into a DataFrame
        product_details_data = pd.read_sql(query, conn)
        
        # Print the data
        print(product_details_data)

except pyodbc.Error as e:
    print("Error connecting to the database:", e)
