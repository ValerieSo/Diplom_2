import pytest
from data.helpers import Generators
from base_api_methods import UserAPI


@pytest.fixture(scope='function')
def registration_user_data():
    email = Generators.generate_random_email()
    password = Generators.generate_random_password()
    name = Generators.generate_random_name()
    return {"email": email, "password": password, "name": name}


@pytest.fixture(scope='function')
def create_and_delete_user(registration_user_data):
    payload = registration_user_data
    response = UserAPI.response_create_user(payload)
    access_token = response.json()['accessToken']
    yield payload, access_token
    headers = {'Authorization': access_token}
    UserAPI.delete_user(headers)
