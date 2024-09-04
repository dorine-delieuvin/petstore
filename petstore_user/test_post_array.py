import pytest
import requests
import random
import create

pytestmark = pytest.mark.user


def test_post_array():
    # set up array
    array = [
        {
            "id": random.randint(1, 99999999999),
            "username": "Bob" + str(random.randint(0, 10000)),
            "firstName": "Troll",
            "lastName": "Noob",
            "email": "troll.noob@email.com",
            "password": "pw123",
            "phone": "07" + str(random.randint(000000000, 999999999)),
        },
        {
            "id": random.randint(1, 99999999999),
            "username": "Bob" + str(random.randint(0, 10000)),
            "firstName": "Robert",
            "lastName": "Junior",
            "email": "robby.jr@email.com",
            "password": "pw456",
            "phone": "07" + str(random.randint(000000000, 999999999)),
        },
        {
            "id": random.randint(1, 99999999999),
            "username": "Bob" + str(random.randint(0, 10000)),
            "firstName": "Bobby",
            "lastName": "Duppy",
            "email": "bobby.duppy@email.com",
            "password": "pw789",
            "phone": "07" + str(random.randint(000000000, 999999999)),
        },
    ]

    # post array
    post_array_response = post_array(array)
    assert post_array_response.status_code == 200

    # check all users have been created
    for i in array:
        get_user_response = get_user(array[array.index(i)]["username"])
        assert get_user_response.status_code == 200

        # check user info
        get_user_data = get_user_response.json()
        assert get_user_data["id"] == array[array.index(i)]["id"]
        assert get_user_data["firstName"] == array[array.index(i)]["firstName"]
        assert get_user_data["lastName"] == array[array.index(i)]["lastName"]
        assert get_user_data["email"] == array[array.index(i)]["email"]


## API calls
def post_array(array):
    return requests.post(
        "https://petstore.swagger.io/v2/user/createWithArray", json=array
    )


def get_user(user_name):
    return requests.get(f"https://petstore.swagger.io/v2/user/{user_name}")
