import pytest

from app import app
import json

from flask import jsonify, make_response

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_myapp_create(client):
    json_content = {
        "key" : "me",
        "value": "mine"
    }
    res = client.post("/api/myapp/", data=json_content)
    assert res.status_code == 200



def test_myapp_get(client):
    res = client.get("/api/myapp/me")

    assert res.status_code == 200


def test_myapp_put_or_update(client):
    json_content = {
        "key": "me",
        "value": "I"
    }
    res = client.put("/api/myapp/me", json=json_content)

    assert res.status_code == 200


def test_myapp_delete(client):
    res = client.delete("/api/myapp/me")

    assert res.status_code == 200