import pytest
import requests
import uuid

#python -m pytest -v -s .\test_store.py

endpoint = "https://petstore.swagger.io"

def test_get_endpoint():
    response = requests.get(endpoint)
    assert response.status_code == 200
    
    data = response.json()
    print(data)


def new_order():
    order_id = f"test_order_id_{uuid.uuid4().hex}"
    pet_id = f"test_pet_id_{uuid.uuid4().hex}"
    return {
        "id": order_id,
        "petId": pet_id,
        "quantity": 0,
        "shipDate": "2024-07-19T20:13:11.282Z",
        "status": "placed",
        "complete": True
    }