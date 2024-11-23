from app import db

class Product(db.Model):
    __tablename__ = 'Product'

    ProductID = db.Column("ProductID", db.Integer, primary_key=True)  # Keep the Id as is
    ProductName = db.Column("ProductName", db.String(50), nullable=False)  # Match the database column name
    SupplierID = db.Column("SupplierID", db.Integer, referenced_key=True)    # Match the database column name
    
    __tablename__ = 'Suppliers'

    SupplierID = db.Column("SupplierID", db.Integer, primary_key=True)  # Keep the Id as is
    SupplierName = db.Column("SupplierName", db.String(50), nullable=False)  # Match the database column name
    
    
    def __repr__(self):
        return f'<Product {self.ProductName} {self.SupplierName}>'
    



