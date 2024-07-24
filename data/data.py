from data.helpers import Generators


class StatusCode:

    BAD_REQUEST = 400
    OK = 200
    FORBIDDEN = 403
    UNAUTHORIZED = 401
    INTERNAL_SERVER_ERROR = 500


class StatusResponse:
    USER_ALREADY_EXISTS = "User already exists"
    NOT_ENOUGH_DATA = "Email, password and name are required fields"
    LOGIN_FAILED = "email or password are incorrect"
    EMAIL_TAKEN = "User with such email already exists"
    NEED_AUTHORIZATION = "You should be authorised"
    NEED_INGREDIENTS = "Ingredient ids must be provided"


class TestData:
    TEST_LOGIN_PAYLOAD = {
        "email": "zeitan@yandex.ru",
        "password": "birdybo"
    }

    TEST_LOGIN_PAYLOAD_INVALID_EMAIL = {
        "email": "invalid_email",
        "password": "birdybo"
    }

    TEST_LOGIN_PAYLOAD_INVALID_PWD = {
        "email": "zeitan@yandex.ru",
        "password": "invalid_pwd"
    }

    EXISTING_EMAIL = "zeitan@yandex.ru"

    INCORRECT_INGREDIENTS = {"ingredients": [Generators.generate_random_string(8)]}
