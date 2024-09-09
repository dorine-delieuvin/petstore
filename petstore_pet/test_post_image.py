import pytest
import requests

pytestmark = pytest.mark.pet


def test_post_image(new_pet):
    # create pet
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # upload image
    pet_id = post_pet_response.json()["id"]

    image_name = "test_image.jpg"
    image_path = f"C:\\Users\\Administrator\\Documents\\Workspace\\web_app_testing\\pet_api\\petstore_pet\\{image_name}"
    image = {"file": open(image_path, "rb")}

    post_image_response = post_image(pet_id, image)
    assert post_image_response.status_code == 200
    assert image_name in post_image_response.json()["message"]


## API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def post_image(pet_id, image):
    return requests.post(
        f"https://petstore.swagger.io/v2/pet/{pet_id}/uploadImage", files=image
    )
