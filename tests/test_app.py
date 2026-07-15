import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient  #TestClient lets us make fake HTTP requests to our API
from app import app


client = TestClient(app)# Create a test client that can send requests to the API.

def test_get_characters():
    response = client.get("/characters/")    # Send a GET request to retrieve every character.

    assert response.status_code == 200     # The request should succeed.
    assert isinstance(response.json(), list)     # The endpoint should return a JSON list.

def test_get_characters_name():
    response = client.get("/characters/Jicho")     # Request a character that should exist.

    assert response.status_code == 200
    assert response.json()["name"] == "Jicho"     # Verifying the correct character was returned.

def test_get_characters_fake_name():
    response = client.get("/characters/Dave")     # Requesting a character that does not exist.

    assert response.status_code == 404     # The API should return "Not Found."

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
        "/login/?username=Kenny&password=Cheesecake"     # Send valid login credentials.
    )

    assert response.status_code == 200
    assert "access_token" in response.json()     # A successful login should return a JWT access token.

def test_character_create():
    response = client.post("/characters/?name=Jeho&region_id=2")
    assert response.status_code == 200
    assert response.json()["name"] == "Jeho"      # Verify the API returned the correct character information.
    assert response.json()["region_id"] == 2

def test_character_dupe():
    response = client.post("/characters/?name=Amara&region_id=2")
    assert response.status_code == 400


def test_region_create():
    response = client.post("/regions/?region_id=93&name=lops")
    assert response.status_code == 200
    assert response.json()["id"] == 93
    assert response.json()["name"] == "lops"

def test_region_dupe():
    response = client.post("/regions/?region_id=1&name=Asgard")
    assert response.status_code == 400

def test_character_update():
    response = client.put("/characters/?character_id=2&updated_name=Amaros&new_region_id=1")
    assert response.status_code == 200
    assert response.json()["character_id"] == 2
    assert response.json()["updated_name"] == "Amaros"
    assert response.json()["new_region_id"] == 1

def test_character_delete():
    response = client.delete("/characters/?character_id=13")
    assert response.status_code == 200
