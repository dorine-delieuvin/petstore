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


# python -m pytest -v -s .\test_pet.py::test_get_pet_by_status
def test_get_pet_by_status():
    # test variables
    status = [None, "available", "pending", "sold"]
    tested_status = status[1]

    # create pets with tested_status
    pet1 = new_pet()
    pet2 = new_pet()
    pet1["status"], pet1["name"] = tested_status, "my pet 1"
    pet2["status"], pet2["name"] = tested_status, "my pet 2"

    post_pet1_response = post_pet(pet1)
    post_pet2_response = post_pet(pet2)
    assert post_pet1_response.status_code and post_pet2_response.status_code == 200

    # find pets by tested status
    get_pet_by_status_response = get_pet_by_status(tested_status)
    assert get_pet_by_status_response.status_code == 200

    # check all pets in response have correct tested status
    get_pet_by_status_data = get_pet_by_status_response.json()

    for pet in get_pet_by_status_data:
        assert pet["status"] == tested_status, "Incorrect statuses in response"

    # check if created IDs in response
    pet1_id = pet1["id"]
    pet2_id = pet2["id"]
    found = 0

    for pet in get_pet_by_status_data:
        if pet["id"] == pet1_id:
            found += 1
        elif pet["id"] == pet2_id:
            found += 1
    if found != 2:
        print("Created pets with tested status not found.")
        raise Exception


# python -m pytest -v -s .\test_pet.py::test_get_pet_by_several_statuses
def test_get_pet_by_several_statuses():
    '''
    NOTE: when selecting more than one status in the search, only the first status is returned in the response.
    '''
    # test variables
    status = [None, "available", "pending", "sold"]
    no_status = status[0]
    status1 = status[1]
    status2 = status[2]
    status3 = status[3]
    tested_statuses = status2, status3

    # create pets with tested statuses
    pet1 = new_pet()
    pet2 = new_pet()
    pet3 = new_pet()
    pet1["status"], pet1["name"] = status1, "my pet 1"
    pet2["status"], pet2["name"] = status2, "my pet 2"
    pet3["status"], pet3["name"] = status3, "my pet 3"

    post_pet1_response = post_pet(pet1)
    post_pet2_response = post_pet(pet2)
    post_pet3_response = post_pet(pet3)
    assert post_pet1_response.status_code and post_pet2_response.status_code and post_pet3_response.status_code == 200

    # find pets by tested statuses
    get_pet_by_status_response = get_pet_by_status(status2, status3)
    assert get_pet_by_status_response.status_code == 200

    # check all pets in response have correct tested statuses
    get_pet_by_status_data = get_pet_by_status_response.json()
    returned_statuses = []
    for pet in get_pet_by_status_data:
        print(pet["status"])
        if pet["status"] not in returned_statuses:
            returned_statuses.append(pet["status"])
        assert pet["status"] in tested_statuses, "Incorrect statuses in response"
    assert tested_statuses in returned_statuses, "Missing statuses in response"


# python -m pytest -v -s .\test_pet.py::test_get_pet_by_status_empty
def test_get_pet_by_status_empty():
    '''
    NOTE:
    - exploited the fact "invalid" statuses don't return an error 400.
    - used a made up status ("unused status") without creating a pet to test functionality.
    - as many pets exist for all official status "available", "pending" and "sold", deleting all of them would be time consuming and disturbing other users.
    '''
    # test variables
    status = [None, "available", "pending", "sold", "unused status"]
    tested_status = status[4]

    # do not create pet
    # try to find pets by tested status
    get_pet_by_status_empty_response = get_pet_by_status(tested_status)
    assert get_pet_by_status_empty_response.status_code == 200

    get_pet_by_status_empty_data = get_pet_by_status_empty_response.json()
    assert get_pet_by_status_empty_data == []


# python -m pytest -v -s .\test_pet.py::test_get_pet_by_status_400
def test_get_pet_by_status_400():
    '''
    NOTE: gives 200 even with a status other than "available", "pending" or "sold".
    '''
    # test variables
    invalid_status = [None, "unavailable", "not so valid", "3210", "escaped"]

    # create pets with invalid_status
    i = 0
    response_status_codes = []

    for status in invalid_status:
        # create pet with invalid status
        invalid_pet = new_pet()
        invalid_pet["status"], invalid_pet["name"] = status, "my invalid pet"

        post_invalid_pet_response = post_pet(invalid_pet)
        assert post_invalid_pet_response.status_code == 200

        # find pet by the invalid_status and store response status code
        get_invalid_pet_by_status_response = get_pet_by_status(status)
        response_status_codes.append(get_invalid_pet_by_status_response.status_code)

    print(response_status_codes)
    assert (
        response_status_codes[0]
        and response_status_codes[1]
        and response_status_codes[2]
        and response_status_codes[3]
        and response_status_codes[4]
            ) == 400, f"Fails, at least one status code different from 400: {response_status_codes}"


## API Calls
def post_pet(pet):
    return requests.post(api + "/pet", json=pet)


def get_pet(pet_id):
    return requests.get(api + f"/pet/{pet_id}")


def update_pet(pet):
    return requests.put(api + "/pet", json=pet)


def post_image(pet_id, image):
    return requests.post(api + f"/pet/{pet_id}/uploadImage", files=image)


def get_pet_by_status(status1=None, status2=None, status3=None):
    url = api + f"/pet/findByStatus"

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