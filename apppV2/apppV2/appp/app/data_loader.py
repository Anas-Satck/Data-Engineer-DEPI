#Dataloader.py
import pyodbc
import pandas as pd
from config import Config


laptop_prices = pd.read_csv("database/laptop_prices.csv")
laptop_df = laptop_prices[:5]

def load_laptop_prices():
    return laptop_prices


def load_data():
    connection_string = Config.SQLALCHEMY_DATABASE_URI.replace('mssql+pyodbc:///?odbc_connect=', '')

    conn = pyodbc.connect(connection_string)

    # Define Queries
    Suppliers_query = "SELECT * FROM Suppliers"
    Product_query = "SELECT * FROM Product"
    ProductDetails_query = "SELECT * FROM ProductDetails"
    InventoryLevels_query = "SELECT * FROM InventoryLevels"
    FactSales_query =  "SELECT * FROM FactSales"

    # Fetch as Pandas Dataframes
    Suppliers_df = pd.read_sql(Suppliers_query, conn)
    Product_df = pd.read_sql(Product_query, conn)
    ProductDetails_df = pd.read_sql(ProductDetails_query, conn)
    InventoryLevels_df = pd.read_sql(InventoryLevels_query, conn)
    FactSales_df = pd.read_sql(FactSales_query, conn)

    #Product_df.rename(columns={"Id" : "ProductID"}, inplace=True)
    #ProductDetails_df.rename(columns={"Id" : "ProductDetailsId"}, inplace=True)
    #Suppliers_df.rename(columns={"Id" : "SupplierID"}, inplace=True)
    #FactSales_df.rename(columns={"Id" : "FactSalesId"}, inplace=True)
    #InventoryLevels_df.rename(columns={"Id" : "InventoryLevelsId"}, inplace=True)

    # Merge Suppliers and ProductDetails data
    ProductDetails_Suppliers_df = pd.merge(ProductDetails_df, Suppliers_df, left_on="SupplierID", right_on="SupplierID", how = 'inner')

    # Merge Oder Suppliers with ProductDetails Item
    ProductDetails_Suppliers_Item_df = pd.merge(ProductDetails_Suppliers_df, FactSales_df, left_on="DetailID", right_on="DetailID", how='inner') 

     # Merge ProductDetails_Suppliers_Item_df with Product data
    ProductDetails_Suppliers_Item_Product_df = pd.merge(ProductDetails_Suppliers_Item_df, Product_df, left_on='ProductID', right_on='ProductID', how='inner')

    # Optionally, if you want to include InventoryLevels data
    ProductDetails_Suppliers_Item_Product_InventoryLevels_df = pd.merge(ProductDetails_Suppliers_Item_Product_df, InventoryLevels_df, left_on='InventoryID', right_on='InventoryID', how='inner')

    # Close Connection
    conn.close()

    # print success message
    print("Data frames loaded successfult!")

    Product_df = Product_df[:5]
    Suppliers_df = Suppliers_df[:5]
    ProductDetails_df = ProductDetails_df[:5]
    FactSales_df = FactSales_df[:5]
    InventoryLevels_df = InventoryLevels_df[:5]

    return laptop_df, Suppliers_df, ProductDetails_df, FactSales_df, Product_df, InventoryLevels_df






