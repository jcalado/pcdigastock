import requests
import sys
from bs4 import BeautifulSoup
import re
from colorit import *
import termtables as tt
from pushover import Client
import config
import codecs

init_colorit()

total = 0
totalStock = 0
components = []
titles = []
prices = []
stocks = []
outOfStock = []


def getProducts():
    products = []
    try: 
        with codecs.open('links.txt', 'r', 'utf-8') as file:
            line = file.readline().replace("\r\n","")
            while line:
                products.append(line)
                line = file.readline().replace("\r\n","")
    except Exception as e:
        print('Erro no ficheiro links.txt.')
        raise e
    
    return products

products = getProducts()

for product in products:

    page = requests.get(product)
    content = page.content.decode('utf-8')

    r1 = re.findall("'is_in_stock': 1,", content)

    soup = BeautifulSoup(page.content, 'html.parser')

    inStock = (len(r1) == 1)  
    title =  soup.select_one('title').text
    price = soup.find("meta",  property="product:price:amount")['content']
    total = total + float(price)

    prices.append(price)
    titles.append(title.replace(' | PCDIGA', ''))

    if inStock:
        stock = color("OK", Colors.green)
        totalStock += 1
    else:
        stock = color("SEM STOCK", Colors.red)
        outOfStock.append(title.replace(' | PCDIGA', ''))
    

    stocks.append(stock)

# Table header
header = ["Produto", "Stock", "Preço"]
data = []

# Table contents - Loop products and add details to data var for table printing
for i, product in enumerate(products):
    data.append([titles[i], stocks[i], "€%s" %(prices[i])])

# Table footer
data.append(["", "TOTAL", round(total,2)])

# Print table to STDOUT
tt.print(
    data,
    header=header
)

client = Client(config.clientKey, api_token=config.apiToken)

if totalStock == len(products):
    client.send_message("Todos os %s produtos em stock!" %(totalStock))
else:
    client.send_message("%s de %s em stock. \nIndisponíveis: \n %s" %(totalStock, len(products), '\r\n'.join(outOfStock)))

