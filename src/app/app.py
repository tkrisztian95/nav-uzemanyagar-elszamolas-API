import os
import re
import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify, make_response, abort, url_for, redirect, request

from app.models import FuelAccountNorm
from app.cache import SimpleCache, TTLCache
from app.default_config import Config
import app.utils as utils
import redis
import json

#CACHE = SimpleCache(debug=True)
CACHE = TTLCache(evictAfterMinutes=5, debug=True)
REDIS_CACHE = None


def create_app(config=None):
    app = Flask(__name__)

    # load default configuration
    app.config.from_object(Config)
    # load environment configuration
    if 'FLASK_CONF' in os.environ:
        app.config.from_envvar('FLASK_CONF')
    # load app sepcified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config, silent=False)

    if True == app.config["USE_REDIS_CACHE"]:
        redis_host = app.config["REDIS_HOST_URL"]
        REDIS_CACHE = redis.Redis(host=redis_host)

    @app.route('/')
    def index():
        return redirect(url_for('root'))

    @app.route('/api')
    def root():
        return make_response(jsonify({
            'data': None,
            'links': {
                'self': "http://localhost:5000/api",
                'uzemanyagarak': "http://localhost:5000/api/nav/uzemanyagarak/{year}",
            },
            'meta': buildMetaData("https://www.nav.gov.hu/")
        }), 200)

    @app.route('/api/nav/uzemanyagarak/<year>')
    def getFuelNormByYear(year):
        queryStringDict = request.args
        filters = {k: v for k, v in queryStringDict.items()
                   if k.startswith("filter")}
        orders = {k: v for k, v in queryStringDict.items()
                  if k.startswith("sort")}
        URL = prepareDataSourceURL(year)
        result = doSort(doFilter(doGetData(URL), filters), orders)
        meta = buildMetaData(URL)
        meta['total'] = len(result)
        return assembleJsonApiResponseModel(result, meta)

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

    def prepareDataSourceURL(year):
        if utils.valid_year(year):
            if utils.is_current_year(year):
                URL = "https://www.nav.gov.hu/nav/szolgaltatasok/uzemanyag/uzemanyagarak/uzemanyagar.html"
            else:
                URL = "https://www.nav.gov.hu/nav/archiv/szolgaltatasok/uzemanyag_elszamolas/{}_uzemanyagar.html".format(
                    year)
        return URL

    def doGetData(URL):
        if True == app.config["NO_CACHE"]:
            return crawl_page(URL)
        elif True == app.config["USE_IN_MEMORY_CACHE"]:
            return CACHE.getOrLoad(URL, crawl_page, URL)
        elif True == app.config["USE_REDIS_CACHE"]:
            key = URL
            if REDIS_CACHE.exists(key) == 1:
                print("found in Redis")
                return json.loads(REDIS_CACHE.get(key), object_hook=lambda d: FuelAccountNorm(**d))
            else:
                data = crawl_page(URL)
                REDIS_CACHE.set(key, json.dumps(serialize(data)))
                print("stored in Redis")
                return data

    def assembleJsonApiResponseModel(data, meta):
        return jsonify(data=serialize(data), meta=meta)

    def buildMetaData(URL):
        return {
            'author': 'Tóth Krisztián Gyula',
            'source': URL
        }

    def doFilter(data, filters):
        if filters is not None:
            for key, value in filters.items():
                attr = re.findall("\[(.*?)\]", key)[0]
                if attr == "month":
                    data = filter_by_month(data, value)
        return data

    def doSort(data, orders):
        if orders is not None:
            for key, value in orders.items():
                attributes = value.split(",")
                for attr in attributes:
                    reverse = False
                    if attr.startswith("-"):
                        attr = attr[1:]
                        reverse = True
                    data.sort(reverse=reverse, key=lambda e: e[attr])
        return data

    def filter_by_month(data, month):
        if utils.valid_month(month):
            return [next((x for x in data if x.month == month), None)]
        return data

    def serialize(data):
        return list(map(lambda item: item.serialize(), data))

    def crawl_page(URL):
        print('crawl_page({})'.format(URL))
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
            # Get rid of empty values
            data.append([ele for ele in cols if ele])

        data = []
        for row in rows:
            cols = row.find_all('td')
            data_item = FuelAccountNorm(
                month=cols[0].text, benzin=cols[1].text, diesel=cols[2].text, mixed=cols[3].text, lpg=cols[4].text)
            data.append(data_item)
        return data

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
