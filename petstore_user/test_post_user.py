import pytest
import requests
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


def test_post_user_double(new_user):
    """
    NOTE 1: no error message when attempting to create two users with same username.
    NOTE 2: using POST with an existing username updates user info (not specified in API documentation).
    NOTE 3: so the update is what's tested here in the end.
    """
    # create user 1
    new_user["username"] = "Mike" + str(random.randint(0, 10000))

    new_user1 = new_user
    new_user1["firstName"] = "user1"
    new_user1["lastName"] = "USER1"

    post_user_response1 = post_user(new_user1)
    assert post_user_response1.status_code == 200

    # create second user with same username
    new_user2 = {
        "id": new_user1["id"],
        "username": new_user1["username"],
        "firstName": "user2",
        "lastName": "USER2",
        "email": new_user1["email"],
        "password": new_user1["password"],
        "phone": new_user1["phone"],
    }

    post_user_response2 = post_user(new_user2)
    assert post_user_response2.status_code == 200

    # get user details
    get_user_response = get_user(new_user["username"])
    assert get_user_response.status_code == 200

    # check details are updated
    get_user_data = get_user_response.json()
    assert get_user_data["id"] == new_user1["id"] == new_user2["id"]
    assert get_user_data["username"] == new_user1["username"] == new_user2["username"]
    assert (
        get_user_data["firstName"] == new_user2["firstName"] != new_user1["firstName"]
    )
    assert get_user_data["lastName"] == new_user2["lastName"] != new_user1["lastName"]


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


## API calls
def post_user(user):
    return requests.post("https://petstore.swagger.io/v2/user", json=user)


def get_user(user_name):
    return requests.get(f"https://petstore.swagger.io/v2/user/{user_name}")
