from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Product
from app.forms import ProductForm  # Adjusted to use the simple form class
from app.data_loader import laptop_prices, load_laptop_prices, load_data


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Retrieve form data

        form = ProductForm()

        # Create a new Sale instance
        new_Product = Product(
            ProductName=form.ProductName,
            SupplierName=form.SupplierName,
     #        city=form.city,
     #       country=form.country,
     #     phone=form.phone
        )
        db.session.add(new_Product)  # Add to session
        db.session.commit()  # Commit the session to save changes
        return redirect(url_for('main.home'))  # Redirect to home after adding

    return render_template('home.html')  # Render home template

@main.route('/dataframes')
def display_dataframes():
    # Load Dataframes From Database
    laptop_df, Suppliers_df,  ProductDetails_df, InventoryLevels_df, Product_df, FactSales_df = load_data()

    #Convert Dataframes to HTML tables
    laptop_html = laptop_df.to_html(classes = 'data', header = True, index = False)
    Suppliers_html = Suppliers_df.to_html(classes = 'data', header = True, index = False)
    ProductDetails_html =  ProductDetails_df.to_html(classes = 'data', header = True, index = False)
    InventoryLevels_html = InventoryLevels_df.to_html(classes = 'data', header = True, index = False)
    FactSales_html = FactSales_df.to_html(classes = 'data', header = True, index = False)
    Products_html = Product_df.to_html(classes = 'data', header = True, index = False)

    return render_template('dataframes.html', laptop = laptop_html, Suppliers = Suppliers_html,
                           ProductDetails = ProductDetails_html, InventoryLevels = InventoryLevels_html, 
                           FactSales = FactSales_html, Products = Products_html)