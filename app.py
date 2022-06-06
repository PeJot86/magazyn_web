from flask import Flask, render_template, request, redirect, url_for
from forms import Product, ProductForm
import csv


items = [{"name" : "mleko","quantity": 10,"unit": "litr","unit_price": 2},
        {"name" : "cukier","quantity": 10,"unit": "kg","unit_price": 4},
        {"name" : "chleb","quantity": 10,"unit": "szt","unit_price": 5}]



app = Flask(__name__)
app.config["SECRET_KEY"] = "mix"


@app.route("/")
def homepage():
    return render_template("base.html")


@app.route("/products", methods=["GET", "POST"])
def add_product():    
    form = ProductForm ()
    errors = None
    list_items = items
    if request.method == 'POST':
        if form.validate_on_submit():
                dict = { 
                "name" : form.name.data, 
                "quantity": form.quantity.data, 
                "unit": form.unit.data,
                "unit_price":form.unit_price.data}
                list_items.append(dict)

        # return redirect(url_for("add_product"))
    return render_template ("list_product.html", form=form, list_items = list_items, errors = errors)
    







if __name__ == "__main__":
    app.run(debug=True)