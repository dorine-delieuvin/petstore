import requests
import random


def new_pet(
    pet_name="doggie",
    status="available",
    category_name="test category name",
    photo_url="my_photo_url",
    tag_name="my tag name",
):
    pet_id = random.randint(1, 99999999999)

    pet = {
        "id": pet_id,
        "category": {
            # "id": 0, # set to 0 by default server side
            "name": category_name
        },
        "name": pet_name,
        "photoUrls": [photo_url],
        "tags": [
            {
                # "id": 0, # set to 0 by default server side
                "name": tag_name
            }
        ],
        "status": status,
    }

    post_pet_response = requests.post("https://petstore.swagger.io/v2/pet", json=pet)
    assert post_pet_response.status_code == 200
    post_pet_data = post_pet_response.json()
    return post_pet_data


if __name__ == "__main__":
    print(new_pet())
