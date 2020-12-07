import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify, make_response, abort

from models import FuelAccountNorm
import utils

app = Flask(__name__)
# add UTF-8 support
app.config['JSON_AS_ASCII'] = False


@app.route('/api')
def root():
    return make_response(jsonify({
        'data': None,
        'links': {
            'self': "http://localhost:5000/api",
            'uzemanyagarak': "http://localhost:5000/api/nav/uzemanyagarak/{year}/{month}",
        }
    }), 200)


@app.route('/api/nav/uzemanyagarak/<year>')
def getFuelNormByYear(year):
    if utils.valid_year(year):
        if utils.is_current_year(year):
            return getFromCurrentYear(None)
        else:
            return getFromArchived(year, None)
    return


@app.route('/api/nav/uzemanyagarak/<year>/<month>')
def getFuelNormByMonth(year, month):
    if utils.valid_year(year) and utils.valid_month(month):
        if utils.is_current_year(year):
            return getFromCurrentYear(month)
        else:
            return getFromArchived(year, month)
    return


def getFromCurrentYear(month):
    URL = "https://www.nav.gov.hu/nav/szolgaltatasok/uzemanyag/uzemanyagarak/uzemanyagar.html"
    data = crawl_page(URL)
    if month != None:
        data = filter_by_month(data, month)
    return jsonify(data=serialize(data))


def getFromArchived(year, month):
    URL = "https://www.nav.gov.hu/nav/archiv/szolgaltatasok/uzemanyag_elszamolas/{}_uzemanyagar.html".format(
        year)
    data = crawl_page(URL)
    if month != None:
        data = filter_by_month(data, month)
    return jsonify(data=serialize(data))


def filter_by_month(data, month):
    return [next((x for x in data if x.month == month), None)]


def serialize(data):
    return list(map(lambda item: item.serialize(), data))


def crawl_page(URL):
    page = requests.get(URL)
    if page.status_code == 404:
        abort(404)

    soup = BeautifulSoup(page.content, 'html.parser')
    data = []
    table_container = soup.find('div',  class_="CikkArticleTableBorder")
    table = table_container.find('table')

    rows = table.find_all('tr')
    rows.pop(0)  # Get rid of table headers
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values

    data = []
    for row in rows:
        cols = row.find_all('td')
        data_item = FuelAccountNorm(
            month=cols[0].text, benzin=cols[1].text, diesel=cols[2].text, mixed=cols[3].text, lpg=cols[4].text)
        data.append(data_item)
    return data


@app.errorhandler(404)
def not_found(e):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': 'invalid resource URI'})
    status_code = 404
    return make_response(response, status_code)


@app.errorhandler(500)
def internal_server_error(e):
    response = jsonify({'status': 500, 'error': 'internal server error',
                        'message': e.description})
    status_code = 500
    return make_response(response, status_code)
