from flask import Flask, render_template, request, redirect, url_for
from forms import  ProductForm
import csv


items = [{"name" : "mleko","quantity": 100,"unit": "litr","unit_price": 2},
        {"name" : "cukier","quantity": 150,"unit": "kg","unit_price": 4},
        {"name" : "chleb","quantity": 180,"unit": "szt","unit_price": 5}]



app = Flask(__name__)
app.config["SECRET_KEY"] = "mix"


@app.route("/")
def homepage():
    return render_template("base.html")


@app.route("/products", methods=["GET", "POST"])
def add_product():    
    form = ProductForm ()
    errors = None
    sort_items = sorted(items, key=lambda x: (x['name']))
    if request.method == 'POST':
        if form.validate_on_submit():
                dict = { 
                "name" : form.name.data, 
                "quantity": form.quantity.data, 
                "unit": form.unit.data,
                "unit_price":form.unit_price.data}
                items.append(dict)
                 
        return redirect(url_for("add_product"))
    return render_template ("list_product.html", form=form, list_items = sort_items, errors = errors)
    

@app.route('/<product_name>', methods=["GET", "POST"])
def edit_product(product_name):    
    form = ProductForm ()
    select_item = (list(filter(lambda x: x['name'] == product_name, items)))
    if request.method == 'POST':
           for i in select_item:
                i["name"] = product_name
                i["quantity"] = float(form.quantity.data)
                i["unit"] = form.unit.data
                i["unit_price"] = float(form.unit_price.data)          
           return redirect(url_for("add_product"))     
    return render_template ("edit_product.html", form=form, product_name= product_name, select_item = select_item)


@app.route('/delete/<product_name>', methods=["GET","POST"])
def delete_product(product_name):    
    form = ProductForm ()
    for i in range(len(items)):
        if items[i]['name'] == product_name:
            del items[i]
            break
    return render_template ("edit_product.html", form=form, product_name= product_name)



if __name__ == "__main__":
    app.run(debug=True)