import pytest
import requests

pytestmark = pytest.mark.pet


def test_delete_pet(new_pet):
    # create pet
    new_pet["name"] = "Butter"
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200
        
    # check pet is created
    pet_id = post_pet_response.json()["id"]
    
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200
    assert get_pet_response.json()["name"] == new_pet["name"]
    
    # delete pet
    delete_pet_response = delete_pet(pet_id)
    assert delete_pet_response.status_code == 200
    
    # check pet is deleted
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 404
    assert get_pet_response.json()["message"] == "Pet not found", f"Message returned: {get_pet_response.json()["message"]}"


def test_delete_pet_unused_id():
    # ensure tested id is unused
    unused_pet_id = 00000
    get_unused_id_response = get_pet(unused_pet_id)
    assert get_unused_id_response.status_code == 404
    
    # attempt to delete inexisting pet
    delete_pet_response = delete_pet(unused_pet_id)
    assert delete_pet_response.status_code == 404


## API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def get_pet(pet_id):
    return requests.get(f"https://petstore.swagger.io/v2/pet/{pet_id}")


def delete_pet(pet_id):
    return requests.delete(f"https://petstore.swagger.io/v2/pet/{pet_id}")
