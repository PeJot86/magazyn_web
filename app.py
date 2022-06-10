from flask import Flask, render_template, request, redirect, url_for
from forms import  ProductForm, SellForm
from function import *
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "mix"
load_items_from_csv()
load_sales_from_csv()


@app.route("/")
def homepage():
    return render_template("base.html")


@app.route("/products", methods=["GET", "POST"])
def add_product():    
    form = ProductForm ()
    sort_items = sorted(items, key=lambda x: (x['name']))
    if request.method == 'POST':
        if form.validate_on_submit():
                dict = { 
                "name" : form.name.data, 
                "quantity": float(form.quantity.data), 
                "unit": form.unit.data,
                "unit_price": float(form.unit_price.data)}
                items.append(dict)
                export_items_to_csv()
        return redirect(url_for("add_product"))
    return render_template ("list_product.html", form=form, list_items = sort_items)
    

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
                export_items_to_csv()
           return redirect(url_for("add_product"))     
    return render_template ("edit_product.html", form=form, product_name= product_name, select_item = select_item)


@app.route('/delete/<product_name>')
def delete_product(product_name):    
    form = ProductForm ()
    for i in range(len(items)):
        if items[i]['name'] == product_name:
            del items[i]
            break
        export_items_to_csv()
    return redirect(url_for("add_product"))   


@app.route('/sell/<product_name>', methods=["GET", "POST"])
def sell_product (product_name):
    form = ProductForm ()
    sell_quantity = 1
    for i in items:
        if  i['name'] == product_name:
            quant_numb = i['quantity']
            sell_quant_sum = quant_numb - sell_quantity
            i['quantity'] = sell_quant_sum
            sold_list.append ({"name": product_name, "quantity" : sell_quantity, "unit" : i["unit"], "unit_price" : i["unit_price"]})
            export_items_to_csv()
            export_sales_to_csv()
    return redirect(url_for("add_product"))   


@app.route("/revenue", methods=["GET", "POST"])
def costs_items ():
    form = SellForm ()
    return render_template ("revenue.html", form=form)


@app.context_processor
def show_costs ():
    sum_list=[]
    for i in items:
        sum_list.append(i["quantity"] * i["unit_price"])
    sum_value = (sum(sum_list))
    rounded_sum = round(sum_value, 2)
    return dict(sum_value=rounded_sum)


@app.context_processor
def get_income ():
    sub_list = []
    for i in sold_list:
        sub_list.append (i["quantity"] * i["unit_price"])
    sold_value = (sum(sub_list))
    rounded_value = round(sold_value, 2)
    return dict(sold_value=rounded_value)


@app.context_processor
def sell_margin ():
    sub_list = []
    for i in sold_list:
        sub_list.append (i["quantity"] * i["unit_price"])
    margin = 0.20 #20% margin
    sold_value = (sum(sub_list)) * margin
    rounded_margin = round(sold_value, 2)
    return dict(margin_value=rounded_margin)
  

@app.context_processor   
def show_revenue ():
    profit = get_income()
    cost = show_costs()
    margin = sell_margin()
    profit_v = (list(profit.values()))
    cost_v = (list(cost.values()))
    margin_v = (list(margin.values()))
    one = (', '.join(map(str, profit_v)))
    two = (', '.join(map(str, cost_v)))
    three = (', '.join(map(str, margin_v)))
    revenue = float(one) + float(three) - float(two)
    rounded_revenue = round (revenue, 2)
    return dict(revenue=rounded_revenue)


@app.context_processor
def date_time ():
    d = datetime.datetime.now()
    return dict(day=(f"{d:%d}"), month=(f"{d:%m}"), year=d.year, hour=(f"{d:%H}"), minute=(f"{d:%M}"))


if __name__ == "__main__":
    app.run(debug=True)
   