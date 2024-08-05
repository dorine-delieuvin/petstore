import pytest
import requests
import random

# python -m pytest -v -s .\test_pet.py::test_post_image

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
    # should fail, correct name: "doggie"
    try:
        assert get_pet_data["name"] == ["douggie"]
    except:
        print("Failed as intended.")


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
    # update_pet_data = update_pet_response.json()
    # print("UPDATE_PET DATA:", update_pet_data)
    assert update_pet_response.status_code == 200

    # get updated pet, check new data
    get_updated_pet_response = get_pet(pet_id)
    assert get_updated_pet_response.status_code == 200

    get_updated_pet_data = get_updated_pet_response.json()
    # print("UPDATED DATA:", get_updated_pet_data)
    assert get_updated_pet_data["name"] == updated_pet["name"]
    assert get_updated_pet_data["status"] == updated_pet["status"]


def test_post_image():
    # create pet
    pet = new_pet()
    post_pet_response = post_pet(pet)
    assert post_pet_response.status_code == 200

    pet_id = post_pet_response.json()["id"]

    # upload image
    image_name = "test_image.jpg"
    image_path = f"C:\\Users\\Administrator\\Documents\\Workspace\\web_app_testing\\pet_api\\{image_name}"
    image = {"file": open(image_path, "rb")}

    post_image_response = post_image(pet_id, image)
    assert post_image_response.status_code == 200

    # check image data
    post_image_data = post_image_response.json()
    assert image_name in post_image_data["message"]


## API Calls
def post_pet(pet):
    return requests.post(api + "/pet", json=pet)


def get_pet(pet_id):
    return requests.get(api + f"/pet/{pet_id}")


def update_pet(pet):
    return requests.put(api + "/pet", json=pet)


def post_image(pet_id, image):
    return requests.post(api + f"/pet/{pet_id}/uploadImage", files=image)


def new_pet():
    pet_id = random.randint(10000, 1000000000000)

    return {
        "id": pet_id,
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
