import pytest

from app import app

from flask import jsonify, make_response


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    res = client.get('/api/')
    #mock_response = b'[{"content":"1 : one","message":"Welcome to my app"},200]'
    print(res.data)
    assert res.status_code == 200
    assert b'"message": "Welcome to my app"' in res.data
    assert b'"content": "1 : one"' in res.data


