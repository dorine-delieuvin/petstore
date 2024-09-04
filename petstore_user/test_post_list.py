import pytest
import requests
import random

pytestmark = pytest.mark.user


def test_post_list():
    # set up list
    list = [
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

    # post list
    post_list_response = post_list(list)
    assert post_list_response.status_code == 200

    # check all users have been created
    for i in list:
        get_user_response = get_user(list[list.index(i)]["username"])
        assert get_user_response.status_code == 200

        # check user info
        get_user_data = get_user_response.json()
        assert get_user_data["id"] == list[list.index(i)]["id"]
        assert get_user_data["firstName"] == list[list.index(i)]["firstName"]
        assert get_user_data["lastName"] == list[list.index(i)]["lastName"]
        assert get_user_data["email"] == list[list.index(i)]["email"]


## API calls
def post_list(list):
    return requests.post(
        "https://petstore.swagger.io/v2/user/createWithList", json=list
    )


def get_user(user_name):
    return requests.get(f"https://petstore.swagger.io/v2/user/{user_name}")
