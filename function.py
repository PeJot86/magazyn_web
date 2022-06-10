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


def export_sales_to_csv():
    with open('Magazyn_sold.csv', mode='w', encoding="utf-8") as csv_file:
        fieldnames = ['name', 'quantity', 'unit', 'unit_price']
        csvwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csvwriter.writeheader()
        for n in sold_list:
            csvwriter.writerow(n)


def load_sales_from_csv():
    with open('Magazyn_sold.csv', newline='', encoding="utf-8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for i in csvreader:
            sold_list.append ({"name" : i['name'], "quantity" : float(i['quantity']), "unit" : i['unit'], "unit_price" : float(i['unit_price'])})


items = []
sold_list = []

