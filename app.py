from flask import Flask, render_template, request, redirect, url_for
from forms import Product, ProductForm
import csv


items = [  
        Product ("mleko", 100, "litr", 5),
        Product ("cukier", 100, "kg", 6.5),
        Product  ("chleb", 20, "szt", 7.5)]


app = Flask(__name__)
app.config["SECRET_KEY"] = "ni"


@app.route("/")
def homepage():
    return render_template("base.html")


# @app.route("/products", methods=["GET", "POST"])
# def list_product():
#     form = ProductForm
#     list_items = items
#     # by_name = sorted(items, key=lambda x: x.name)
#     return render_template ("list_product.html", list_items = list_items, form=form)


@app.route("/products", methods=["GET", "POST"])
def add_product():    
    form = ProductForm ()
    errors = None
    list_items = items
    if request.method == 'POST':
        if form.validate_on_submit():
                product = Product(
                    name=form.name.data,
                    quantity=form.quantity.data,
                    unit=form.unit.data,
                    unit_price=form.unit_price.data
            )
                (items.append (product))
        return redirect(url_for("add_product"))
    return render_template ("list_product.html", form=form, list_items = list_items, errors = errors)






# sold_list = [] #lista sprzedanych tow.

# def load_items_from_csv():
#     with open('Magazyn.csv', newline='') as csvfile:
#         csvreader = csv.DictReader(csvfile)
#         for i in csvreader:
#             items.append ({"Name" : i['Name'], "Quantity" : float(i['Quantity']), "Unit" : i['Unit'], "Unit_price" : float(i['Unit_price'])})

# def export_items_to_csv():
#     with open('Magazyn.csv', mode='w') as csv_file:
#         fieldnames = ['Name', 'Quantity', 'Unit', 'Unit_price']
#         csvwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
#         csvwriter.writeheader()
#         for n in items:
#             csvwriter.writerow(n)

# def export_sales_to_csv():
#     with open('Magazyn_sold.csv', mode='w') as csv_file:
#         fieldnames = ['Name', 'Quantity', 'Unit', 'Unit_price']
#         csvwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
#         csvwriter.writeheader()
#         for n in sold_list:
#             csvwriter.writerow(n)

# def costs_items (items):
#     sum_list = []
#     for i in items:
#         sum_list.append (i["Quantity"] * i["Unit_price"])
#     return sum(sum_list)

# def print_costs_items (items):
#     cost = costs_items(items)
#     print (f"Koszt zakupu towarów to: {cost} PLN")

# def get_income (sold_list):
#     sub_list = []
#     for i in sold_list:
#         sub_list.append (i["Quantity"] * i["Unit_price"])
#     return sum(sub_list)
    
# def print_get_income (items):
#     profit = get_income (sold_list)
#     print (f"Zyski uzyskane ze sprzedaży towarów to: {profit} PLN")

# def show_revenue ():
#     profit = get_income (sold_list)
#     cost = costs_items (items)
#     revenue = profit - cost
#     print (f"Bilans Twoich zysków to: {revenue}")




# def add_items (name, quantity, unit, price):
#     dict = {"Name": name, "Quantity" : quantity, "Unit" : unit, "Unit_price" : price}
#     items.append(dict)
#     get_items ()
#     print (f"\nDODAŁEM: {name}")

# def sell_items (sell_name, sell_quantity):
#     for i in items:
#         if  i['Name'] == sell_name:
#             quant_numb = i['Quantity']
#             sell_quant_sum = quant_numb - sell_quantity
#             i['Quantity'] = sell_quant_sum
#             sold_list.append ({"Name": sell_name, "Quantity" : sell_quantity, "Unit" : i["Unit"], "Unit_price" : i["Unit_price"]})
#             print (f"Sprzedaję {sell_quantity} {sell_name}, pozostało {sell_quant_sum}")


if __name__ == "__main__":
    app.run(debug=True)