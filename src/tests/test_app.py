# Third party modules
import pytest
import json
import app

# First party modules
from app import app
from app.app import create_app
from app.models import FuelAccountNorm


@pytest.fixture
def client():
    app = create_app("../conf/test_config.py")
    with app.test_client() as client:
        yield client


def test_uzemanyagarak_2020(client):
    rv = client.get("/api/nav/uzemanyagarak/2020")
    response_json = json.loads(rv.data)
    assert 12 == len(response_json['data'])

def test_uzemanyagarak_2020_január(client):
    rv = client.get("/api/nav/uzemanyagarak/2020/január")
    response_json = json.loads(rv.data)
    assert 1 == len(response_json['data'])
    first_item_dict = response_json['data'][0]
    fuelAccountNorm_object = FuelAccountNorm(**first_item_dict)
    assert 'január' == fuelAccountNorm_object.month

def test_uzemanyagarak_2020_január_meta_returned(client):
    rv = client.get("/api/nav/uzemanyagarak/2020/január")
    response_json = json.loads(rv.data)
    assert 'meta' in response_json
    assert "Tóth Krisztián Gyula" == response_json['meta']['author']
    assert 1 == response_json['meta']['total']  

def test_uzemanyagarak_2019(client):
    rv = client.get("/api/nav/uzemanyagarak/2019")
    response_json = json.loads(rv.data)
    assert 12 == len(response_json['data'])

def test_uzemanyagarak_2020_meta_returned(client):
    rv = client.get("/api/nav/uzemanyagarak/2020")
    response_json = json.loads(rv.data)
    assert 'meta' in response_json
    assert "Tóth Krisztián Gyula" == response_json['meta']['author']
    assert 12 == response_json['meta']['total']

def test_root_meta_returned(client):
    rv = client.get("/api")
    response_json = json.loads(rv.data)
    assert 'meta' in response_json
    assert "Tóth Krisztián Gyula" == response_json['meta']['author']