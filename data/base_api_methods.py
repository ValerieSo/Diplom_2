import requests
from data.endpoints import Endpoints


class UserAPI:
    @staticmethod
    def response_create_user(payload):
        response = requests.post(Endpoints.ENDPOINT_CREATE_USER, data=payload)
        return response

    @staticmethod
    def response_login_user(payload):
        response = requests.post(Endpoints.ENDPOINT_LOGIN_USER, data=payload)
        return response

    @staticmethod
    def response_change_user_info(payload, headers):
        response = requests.patch(Endpoints.ENDPOINT_CHANGE_USER_INFO, data=payload, headers=headers)
        return response

    @staticmethod
    def delete_user(headers):
        requests.delete(Endpoints.ENDPOINT_CHANGE_USER_INFO, headers=headers)


class OrderAPI:
    @staticmethod
    def response_get_ingredients():
        response = requests.get(Endpoints.ENDPOINT_GET_INGREDIENTS)
        return response

    @staticmethod
    def response_make_order(payload, headers):
        response = requests.post(Endpoints.ENDPOINT_MAKE_ORDER, data=payload, headers=headers)
        return response

    @staticmethod
    def response_get_user_orders(headers):
        response = requests.get(Endpoints.ENDPOINT_GET_ORDERS_OF_USER, headers=headers)
        return response
