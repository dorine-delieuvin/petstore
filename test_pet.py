import pytest
import requests
import random

# python -m pytest -v -s .\test_pet.py::test_update_pet

endpoint = "https://petstore.swagger.io"
api = endpoint + "/v2"


def test_get_endpoint():
    get_endpoint_response = requests.get(endpoint)
    assert get_endpoint_response.status_code == 200


# python -m pytest -v -s .\test_pet.py::test_post_pet
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
    # should fail:
    assert (
        get_pet_data["name"] == "douggie"
    ), "Failed as intended, correct name: 'doggie'"


# python -m pytest -v -s .\test_pet.py::test_update_pet
def test_update_pet():
    """
    NOTE #1: Sometimes fails to assert the updated pet name.
    NOTE #2: Sometimes returns a 404 instead of 200 when creating a new pet.
    Those are assumed to be due to server activity as the tests pass successfully when re-run most of the time.
    """
    # create pet
    pet = new_pet()
    post_pet_response = post_pet(pet)
    assert post_pet_response.status_code == 200

    pet_id = post_pet_response.json()["id"]
    print("PET ID:", pet_id)

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
    assert update_pet_response.status_code == 200

    # get updated pet, check new data
    get_updated_pet_response = get_pet(pet_id)
    assert get_updated_pet_response.status_code == 200

    get_updated_pet_data = get_updated_pet_response.json()
    assert get_updated_pet_data["name"] == updated_pet["name"]
    assert get_updated_pet_data["status"] == updated_pet["status"]


def test_update_pet_400():
    # testing error 400: Invalid ID supplied
    """
    NOTE: returns an error 500 instead of 400.
    """
    invalid_pet_id = 0.5
    update_invalid_id_response = update_pet(invalid_pet_id)
    assert (
        update_invalid_id_response.status_code == 400
    ), f"Fails, gives a status {update_invalid_id_response.status_code}, instead of 400."


def test_update_pet_404():
    # testing error 404: Pet not found
    """
    NOTE: returns a 200 instead of 404 for any presumed invalid ID tried.
    """
    invalid_pet = {
        "id": -0.5,  # presummed invalid ID
        "name": "Invalid",
        "status": "unavailable",
    }
    update_invalid_pet_response = update_pet(invalid_pet)
    assert (
        update_invalid_pet_response.status_code == 404
    ), f"Fails, gives a status {update_invalid_pet_response.status_code}, instead of 404."


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


# python -m pytest -v -s .\test_pet.py::test_get_pet
def test_get_pet():
    # create pet
    pet = new_pet()
    post_pet_response = post_pet(pet)
    assert post_pet_response.status_code == 200

    pet_id = post_pet_response.json()["id"]
    print(pet_id)

    # get pet
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200

    # check pet info
    get_pet_data = get_pet_response.json()
    assert get_pet_data["id"] == pet_id
    assert get_pet_data["name"] == pet["name"]
    assert get_pet_data["status"] == pet["status"]


# python -m pytest -v -s .\test_pet.py::test_get_pet_404
def test_get_pet_404():
    # don't create pet
    # get pet
    inexistant_pet_id = 0
    get_pet_response = get_pet(inexistant_pet_id)
    assert (
        get_pet_response.status_code == 404
    ), f"Fails, gives a status {get_pet_response.status_code}, instead of 404."


# python -m pytest -v -s .\test_pet.py::test_get_pet_400
def test_get_pet_400():
    """
    NOTE: when providing an invalid pet ID, the API assigns a default ID "9223372036854775807" to the pet instead of returning an error
    """
    # create pet with an invalid ID
    pet = new_pet()
    pet["id"] = -0.5
    post_pet_response = post_pet(pet)
    print(pet["id"])
    assert post_pet_response.status_code == 200

    invalid_pet_id = post_pet_response.json()["id"]
    print(invalid_pet_id)

    # get pet
    get_invalid_pet_response = get_pet(invalid_pet_id)
    assert (
        get_invalid_pet_response.status_code == 400
    ), f"Fails, gives a status {get_invalid_pet_response.status_code}, instead of 400."


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
    pet_id = random.randint(1, 99999999999)

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
