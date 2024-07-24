class Endpoints:
    BASE_URL = 'https://stellarburgers.nomoreparties.site/'
    ENDPOINT_CREATE_USER = f'{BASE_URL}api/auth/register'
    ENDPOINT_LOGIN_USER = f'{BASE_URL}api/auth/login'
    ENDPOINT_CHANGE_USER_INFO = f'{BASE_URL}api/auth/user'
    ENDPOINT_GET_ORDERS_OF_USER = f'{BASE_URL}api/orders'
    ENDPOINT_MAKE_ORDER = f'{BASE_URL}api/orders'
    ENDPOINT_GET_INGREDIENTS = f'{BASE_URL}api/ingredients'
