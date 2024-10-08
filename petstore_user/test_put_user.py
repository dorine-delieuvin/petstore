import pytest
import requests

pytestmark = pytest.mark.user


def test_put_user(new_user, updated_user):
    # create user
    post_user_response = post_user(new_user)
    assert post_user_response.status_code == 200

    # check user has been created
    get_user_response = get_user(new_user["username"])
    assert get_user_response.status_code == 200

    # Merge user with updated data
    merged_user = {**new_user, **updated_user}

    # put user
    put_user_response = put_user(new_user["username"], merged_user)
    assert put_user_response.status_code == 200

    # check updated details are updated
    get_user_response = get_user(new_user["username"])
    assert get_user_response.status_code == 200

    get_user_data = get_user_response.json()
    assert get_user_data["id"] == new_user["id"]
    assert get_user_data["username"] == new_user["username"]
    assert get_user_data["firstName"] != new_user["firstName"]
    assert get_user_data["lastName"] != new_user["lastName"]
    assert get_user_data["phone"] == new_user["phone"]


@pytest.mark.skip
def test_put_user_inexisting_username(updated_user):
    """
    NOTE: getting 200 instead of 404 when trying to update user details using a non-existent username.
    """
    # making sure the user does not exist
    user_name = "Bob456"
    get_user_response = get_user(user_name)
    assert get_user_response.status_code == 404

    get_user_data = get_user_response.json()
    print(get_user_data)

    # attempt to update inexisting user
    put_user_response = put_user(user_name, updated_user)
    assert put_user_response.status_code == 404

    # check body response
    put_user_data = put_user_response.json()
    print(f"PUT: {put_user_data}")
    assert put_user_data["message"] == "User not found"


@pytest.mark.skip
def test_put_user_invalid_username(updated_user):
    """
    NOTE: getting code 200 instead of 400.
    - tried usernames "Bob@!#", "@!#  !*/à$==`", "" (returns 405) and ",".
    """
    # do not create user
    user_name = "Bob@!#"

    # attempt to get user with invalid username
    put_user_response = put_user(user_name, updated_user)
    assert put_user_response.status_code == 400

    # check body response
    put_user_data = put_user_response.json()
    print(put_user_data)
    assert put_user_data["message"] == "Invalid username supplied"


## API Calls
def post_user(user):
    return requests.post("https://petstore.swagger.io/v2/user", json=user)


def get_user(user_name):
    return requests.get(f"https://petstore.swagger.io/v2/user/{user_name}")


def put_user(user_name, updated_user):
    return requests.put(
        f"https://petstore.swagger.io/v2/user/{user_name}", json=updated_user
    )
