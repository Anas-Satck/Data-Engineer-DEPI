from flask import request

class SaleForm:
    def __init__(self):
        self.SupplierName = request.form.get('SupplierName')
        self.ProductName = request.form.get('ProductName')
    ##  self.Ram = request.form.get('Ram')
    ##  self.OS = request.form.get('OS')
    ##  self.Price = request.form.get('Price')
