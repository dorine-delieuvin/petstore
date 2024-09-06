import pytest
import requests
import random

endpoint = "https://petstore.swagger.io"
api = endpoint + "/v2"

## API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def get_pet(pet_id):
    return requests.get(f"https://petstore.swagger.io/v2/pet/{pet_id}")


def update_pet(pet):
    return requests.put("https://petstore.swagger.io/v2/pet", json=pet)


def get_pet_by_status(status1=None, status2=None, status3=None):
    url = "https://petstore.swagger.io/v2/pet/findByStatus"

    if status1 != None:
        url += f"?status={status1}"

    if status2 != None and status1 != None:
        url += f"&status={status2}"
    elif status2 != None:
        url += f"?status={status2}"

    if status3 != None and (status1 != None or status2 != None):
        url += f"&status={status3}"
    elif status3 != None:
        url += f"?status={status3}"

    print(url)
    return requests.get(url)

def post_data_form(pet_id, form):
    return requests.post("https://petstore.swagger.io/v2/pet/{pet_id}", data=form)


def delete_pet(pet_id):
    return requests.delete("https://petstore.swagger.io/v2/pet/{pet_id}")


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

# python -m pytest -v -s .\test_pet.py::test_get_endpoint
@pytest.mark.pet
def test_get_endpoint():
    get_endpoint_response = requests.get(endpoint)
    assert get_endpoint_response.status_code == 200


# python -m pytest -v -s .\test_pet.py::test_post_pet

# python -m pytest -v -s .\test_pet.py::test_update_pet

# python -m pytest -v -s .\test_pet.py::test_post_image

# python -m pytest -v -s .\test_pet.py::test_get_pet

# python -m pytest -v -s .\test_pet.py::test_get_pet_by_status

# python -m pytest -v -s .\test_pet.py::test_post_data_form_name
@pytest.mark.pet
@pytest.mark.pet_data_form



# python -m pytest -v -s .\test_pet.py::test_post_data_form_status
@pytest.mark.pet
@pytest.mark.pet_data_form

# python -m pytest -v -s .\test_pet.py::test_delete_pet
@pytest.mark.pet
@pytest.mark.pet_delete
def test_delete_pet():
    # create pet
    pet = new_pet()
    pet["name"] = "Butter"
    post_pet_response = post_pet(pet)
    assert post_pet_response.status_code == 200
    
    post_pet_data = post_pet_response.json()
    pet_id = post_pet_data["id"]
    print(pet_id)
    print(pet["name"])
    
    # check pet is created
    get_pet_response = get_pet(pet_id)
    get_pet_data = get_pet_response.json()

    assert get_pet_response.status_code == 200, f"Failded, gived code {get_pet_response.status_code} instead of 200"
    assert get_pet_data["name"] == pet["name"]
    
    # delete pet
    delete_pet_response = delete_pet(pet_id)
    assert delete_pet_response.status_code == 200
    
    # check pet is deleted
    get_pet_response = get_pet(pet_id)
    get_pet_data = get_pet_response.json()
    assert get_pet_response.status_code == 404, f"Failded, gived code {get_pet_response.status_code} instead of 404"
    assert get_pet_data["message"] == "Pet not found", f"Message returned: {get_pet_data["message"]}"


# python -m pytest -v -s .\test_pet.py::test_delete_pet_unused_id
@pytest.mark.pet
@pytest.mark.pet_delete
def test_delete_pet_unused_id():
    # ensure tested id is unused
    unused_pet_id = 00000
    get_unused_id_response = get_pet(unused_pet_id)
    assert get_unused_id_response.status_code == 404, f"{get_unused_id_response.status_code} instead of 404"
    
    # do not create pet
    # delete pet
    delete_pet_response = delete_pet(unused_pet_id)
    assert delete_pet_response.status_code == 404, f"Failded, gived code {delete_pet_response.status_code} instead of 404"

