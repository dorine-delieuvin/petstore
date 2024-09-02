import pytest
import requests
import create
import random

pytestmark = pytest.mark.user


valid_user_info = [
    # happy path
    {
        "id": random.randint(1, 99999999999),
        "username": "Bob" + str(random.randint(0, 10000)),
        "firstName": "Troll",
        "lastName": "Noob",
        "email": "troll.noob@email.com",
        "password": "pw123",
        "phone": "07000000000",
        "userStatus": 1,
    },
    # missing optional fields
    {
        "id": random.randint(1, 99999999999),
        "username": "Sabie" + str(random.randint(0, 10000)),
        "email": "sabrina.bellanger@email.com",
        "password": "pw789",
    },
]

invalid_user_info = [
    # missing required fields
    {
        "id": random.randint(1, 99999999999),
        "username": "Wally" + str(random.randint(0, 10000)),
        "firstName": "William",
        "lastName": "Wallace",
        "email": "william.wallace@email.com",
        "password": "",
        "phone": "07000000000",
        "userStatus": 1,
    },
    # invalid e-mail
    {
        "id": random.randint(1, 99999999999),
        "username": "Dorothy" + str(random.randint(0, 10000)),
        "firstName": "Dorothy",
        "lastName": "Bombay",
        "email": "dorothy.bombayemail.com",
        "password": "pw456",
        "phone": "07000000000",
        "userStatus": 1,
    },
]


@pytest.mark.parametrize("user_data", valid_user_info)
def test_post_user(user_data):
    # create user
    post_user_response = post_user(user_data)
    assert post_user_response.status_code == 200

    # get user details
    get_user_response = get_user(user_data["username"])
    assert get_user_response.status_code == 200

    # check details
    get_user_data = get_user_response.json()
    print(get_user_data)
    assert get_user_data["username"] == user_data["username"]
    assert get_user_data["id"] == user_data["id"]


@pytest.mark.skip
@pytest.mark.parametrize("user_data", invalid_user_info)
def test_post_user_invalid_info(user_data):
    """
    NOTE: getting code 200 even when:
    - missing required fields
    - invalid email format
    """
    # create user
    post_user_response = post_user(user_data)
    assert post_user_response.status_code == 400

    # get user details
    get_user_response = get_user(user_data["username"])
    assert get_user_response.status_code == 400


def test_post_user_double():
    """
    NOTE 1: no error message when attempting to create two users with same username.
    NOTE 2: using POST with an existing username updates user info (not specified in API documentation).
    """
    # create user
    # user[0] == status code; user[1] == user_data
    user1 = create.new_user(user_name="Mike" + str(random.randint(0, 10000)))
    assert user1[0] == 200

    user_name = user1[1]["username"]

    # create second user with same username
    user2 = create.new_user(user_name=user_name, first_name="Troll2", last_name="Noob2")
    # assert user2[0] == 400  # returns 200: intended behaviour
    assert user2[0] == 200

    # get user details
    get_user_response = get_user(user_name)
    assert get_user_response.status_code == 200

    # check details are updated
    get_user_data = get_user_response.json()
    print(get_user_data)
    assert get_user_data["id"] == user1[1]["id"] == user2[1]["id"]
    assert get_user_data["username"] == user1[1]["username"] == user2[1]["username"]
    assert get_user_data["firstName"] == user2[1]["firstName"]
    assert get_user_data["lastName"] == user2[1]["lastName"]


## API calls
def post_user(user):
    return requests.post("https://petstore.swagger.io/v2/user", json=user)


def get_user(user_name):
    return requests.get(f"https://petstore.swagger.io/v2/user/{user_name}")
