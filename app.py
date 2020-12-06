import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify

import models
import utils

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/nav/uzemanyagarak/<year>/<month>')
def getFuelNorm(year, month):
    if utils.valid_year(year) and utils.valid_month(month):
        if utils.is_current_year(year):
            return getFromCurrentYear(month)
        else:
            return getFromArchived(year, month)
    return

def getFromCurrentYear(month):
    URL = "https://www.nav.gov.hu/nav/szolgaltatasok/uzemanyag/uzemanyagarak/uzemanyagar.html"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    data = []
    table_container = soup.find('div',  class_="CikkArticleTableBorder")  
    table = table_container.find('table')

    rows = table.find_all('tr')
    rows.pop(0) # Get rid of table headers
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values

    data=[]
    for row in rows:
        cols = row.find_all('td')
        data_item = models.FuelAccountNorm(month=cols[0].text, benzin=cols[1].text, diesel=cols[2].text, mixed=cols[3].text, lpg=cols[4].text)
        data.append(data_item)   

    serialized = next((x for x in data if x.month == month), None).serialize()
    return jsonify(data=serialized)

def getFromArchived(year, month):
    URL = "https://www.nav.gov.hu/nav/archiv/szolgaltatasok/uzemanyag_elszamolas/{}_uzemanyagar.html".format(year)
    return None




