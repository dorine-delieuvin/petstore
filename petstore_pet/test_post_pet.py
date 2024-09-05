import pytest
import requests
import random

endpoint = "https://petstore.swagger.io"
api = endpoint + "/v2"


@pytest.mark.pet
def test_post_pet(new_pet):
    # create pet
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    post_pet_data = post_pet_response.json()

    # check the created pet
    pet_id = post_pet_data["id"]
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200

    # check data are same as the ones pushed
    get_pet_data = get_pet_response.json()
    assert get_pet_data["status"] == new_pet["status"]
    assert get_pet_data["name"] == new_pet["name"]


## API Calls
def post_pet(pet):
    return requests.post(api + "/pet", json=pet)


def get_pet(pet_id):
    return requests.get(api + f"/pet/{pet_id}")
