import pytest
import requests

# python -m pytest -v -s .\test_pet.py::test_update_pet

endpoint = "https://petstore.swagger.io"
api = endpoint + "/v2"


def test_get_endpoint():
    get_endpoint_response = requests.get(endpoint)
    assert get_endpoint_response.status_code == 200


def test_post_pet():
    # create pet
    pet = new_pet()
    post_pet_response = post_pet(pet)
    assert post_pet_response.status_code == 200

    post_pet_data = post_pet_response.json()

    # check the created pet
    pet_id = post_pet_data["id"]
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200

    # check data are same as the ones pushed + correct fail resp
    get_pet_data = get_pet_response.json()
    assert get_pet_data["status"] == pet["status"]
    assert get_pet_data["name"] == pet["name"]
    # assert get_pet_data["name"] == ["douggie"]  # should fail, correct name: "doggie"


def test_update_pet():
    # create pet
    pet = new_pet()
    post_pet_response = post_pet(pet)
    assert post_pet_response.status_code == 200

    pet_id = post_pet_response.json()["id"]
    # print("PET ID:", pet_id)

    # update pet
    updated_pet = {
        "id": pet_id,
        "category": {
            # "id": 0,  # set to 0 by default server side
            "name": "test category name",
        },
        "name": "updated doggie name",
        "photoUrls": ["my_photo_url"],
        "tags": [
            {
                # "id": 0,
                "name": "my tag name"
            }
        ],  # set to 0 by default server side
        "status": "unavailable",
    }
    update_pet_response = update_pet(updated_pet)
    update_pet_data = update_pet_response.json()
    # print("UPDATE_PET DATA:", update_pet_data)
    assert update_pet_response.status_code == 200

    # get updated pet, check new data
    get_updated_pet_response = get_pet(pet_id)
    assert get_updated_pet_response.status_code == 200

    get_updated_pet_data = get_updated_pet_response.json()
    # print("UPDATED DATA:", get_updated_pet_data)
    assert get_updated_pet_data["name"] == updated_pet["name"]
    assert get_updated_pet_data["status"] == updated_pet["status"]


def post_pet(pet):
    return requests.post(api + "/pet", json=pet)


def get_pet(pet_id):
    return requests.get(api + f"/pet/{pet_id}")


def update_pet(pet):
    return requests.put(api + "/pet", json=pet)


def post_image(petId):
    return requests.post(endpoint + f"/pet/{petId}/uploadImage")


def new_pet():
    return {
        # "id": 0, # defined server side
        "category": {
            # "id": 0, # set to 0 by default server side
            "name": "test category name"
        },
        "name": "doggie",
        "photoUrls": ["my_photo_url"],
        "tags": [
            {
                # "id": 0, # set to 0 by default server side
                "name": "my tag name"
            }
        ],
        "status": "available",
    }
