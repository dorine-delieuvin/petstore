import pytest
import requests

pytestmark = pytest.mark.user


def test_get_login(new_user):
    # create user
    post_user_response = post_user(new_user)
    assert post_user_response.status_code == 200

    # log in
    details = [new_user["username"], new_user["password"]]

    get_login_response = get_login(details[0], details[1])
    assert get_login_response.status_code == 200

    # check response body
    get_login_data = get_login_response.json()
    assert "logged in user session:" in get_login_data["message"]


@pytest.mark.skip
def test_get_login_incorrect_details(user):
    """
    NOTE: invalid details passed give a code 200 instead of 400.
    """
    # create user
    post_user_response = post_user(user)
    assert post_user_response.status_code == 200

    # attempt log in
    usernames = [user["username"], "", user["username"]]
    passwords = ["invalidpw", user["password"], ""]

    for i in passwords:
        get_login_response = get_login(
            usernames[passwords.index(i)], passwords[passwords.index(i)]
        )
        assert get_login_response.status_code == 400

        # check response body
        get_login_data = get_login_response.json()
        assert get_login_data["message"] == "Invalid username/password supplied"


def test_get_logout(new_user):
    """
    NOTE: set to success by default according to documentation
    """
    # create user
    post_user_response = post_user(new_user)
    assert post_user_response.status_code == 200

    # log in
    details = [new_user["username"], new_user["password"]]

    get_login_response = get_login(details[0], details[1])
    assert get_login_response.status_code == 200

    # log out
    get_logout_response = get_logout()
    assert get_logout_response.status_code == 200


## API Calls
def post_user(user):
    return requests.post("https://petstore.swagger.io/v2/user", json=user)


def get_login(user_name, password):
    return requests.get(
        f"https://petstore.swagger.io/v2/user/login?username={user_name}&password=%20{password}"
    )


def get_logout():
    return requests.get("https://petstore.swagger.io/v2/user/logout")
