import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_characters():
    response = client.get("/characters/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_characters_name():
    response = client.get("/characters/Jicho")

    assert response.status_code == 200
    assert response.json()["name"] == "Jicho"

def test_get_characters_fake_name():
    response = client.get("/characters/Dave")

    assert response.status_code == 404

def test_get_region():
    response = client.get("/regions/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_region_name():
    response = client.get("/regions/Rema")

    assert response.status_code == 200
    assert response.json()["name"] == "Rema"

def test_get_region_fake_name():
    response = client.get("/regions/Japan")

    assert response.status_code == 404

def test_login():
    response = client.post(
        "/login/?username=Kenny&password=Cheesecake"
    )

    assert response.status_code == 200
    assert "access_token" in response.json()