from flask import Flask, render_template, request, redirect, url_for
from forms import  ProductForm
import csv



def load_items_from_csv():
    with open('Magazyn.csv', newline='', encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for i in csvreader:
            items.append ({"name" : i['name'], "quantity" : float(i['quantity']), "unit" : i['unit'], "unit_price" : float(i['unit_price'])})


def export_items_to_csv():
    with open('Magazyn.csv', mode='w', encoding="utf-8") as csv_file:
        fieldnames = ['name', 'quantity', 'unit', 'unit_price']
        csvwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csvwriter.writeheader()
        for n in items:
            csvwriter.writerow(n)


items = []
sold_list =[]

app = Flask(__name__)
app.config["SECRET_KEY"] = "mix"
load_items_from_csv()



@app.route("/")
def homepage():
    print (items)
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
            del (items[i])
        export_items_to_csv()
    return render_template ("edit_product.html", form=form, product_name= product_name)


@app.route('/sell/<product_name>', methods=["GET", "POST"])
def sell_product (product_name):
    form = ProductForm ()
    sell_quantity = 1
    for i in items:
        if  i['name'] == product_name:
            quant_numb = i['quantity']
            sell_quant_sum = quant_numb - sell_quantity
            i['quantity'] = sell_quant_sum
            sold_list.append ({"Name": product_name, "quantity" : sell_quantity, "unit" : i["unit"], "unit_price" : i["unit_price"]})
            export_items_to_csv()
    return render_template ("list_product.html", form=form, product_name= product_name)        







if __name__ == "__main__":
    app.run(debug=True)
   