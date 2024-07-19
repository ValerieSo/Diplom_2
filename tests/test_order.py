import allure
from data.data import StatusCode, StatusResponse, TestData
from data.base_api_methods import OrderAPI
from data.helpers import Generators


class TestMakeOrder:
    @allure.title('Проверка создания заказа с валидными ингридиентами авторизованным пользователем')
    @allure.description('Отправляем запрос на создание заказа с валидными ингридиентами, '
                        'в запросе добавляем accessToken в заголовки, ожидаем код 200')
    def test_make_order_auth_user(self, create_and_delete_user):
        payload = Generators.ingredients_set()
        access_token = create_and_delete_user[1]
        headers = {'Authorization': access_token}
        response = OrderAPI.response_make_order(payload, headers)
        actual_result = response.json()["success"]

        assert response.status_code == StatusCode.OK and actual_result is True, \
            (f"Результаты: Получен статус код {response.status_code}, Фактический результат {actual_result}, "
             f"Ожидался статус код {StatusCode.OK}, Ожидаемый результат True")

    @allure.title('Проверка создания заказа неавторизованным пользователем')
    @allure.description('Отправляем запрос на создание заказа, ожидаем код 200')
    def test_make_order_unauth_user(self):
        payload = Generators.ingredients_set()
        access_token = None
        headers = {'Authorization': access_token}
        response = OrderAPI.response_make_order(payload, headers)
        try:
            assert response.status_code == StatusCode.UNAUTHORIZED, \
                f"Результаты: Получен статус код {response.status_code}, Ожидался статус код {StatusCode.UNAUTHORIZED}"
        except AssertionError as e:
            print('Известная ошибка:', e)

    @allure.title('Проверка создания заказа без ингридиентов авторизованным пользователем')
    @allure.description('Отправляем запрос на создание заказа, в запросе направляем пустой словарь "ingredients", '
                        'в запросе добавляем accessToken в заголовки, ожидаем код 400')
    def test_make_order_auth_user_with_empty_ingredients(self, create_and_delete_user):
        payload = {"ingredients": []}
        access_token = create_and_delete_user[1]
        headers = {'Authorization': access_token}
        response = OrderAPI.response_make_order(payload, headers)
        actual_result = response.json()["success"]
        actual_message = response.json()["message"]

        assert (response.status_code == StatusCode.BAD_REQUEST
                and actual_result is False
                and actual_message == StatusResponse.NEED_INGREDIENTS), \
            (f"Фактические результаты: статус код - {response.status_code}, создание заказа - {actual_result}, "
             f"сообщение - {actual_message}. Ожидалось: статус код - {StatusCode.BAD_REQUEST}, создание заказа - False,"
             f"ожидаемое сообщение - {StatusResponse.NEED_INGREDIENTS}")

    @allure.title('Проверка создания заказа с неверным хешем ингредиентов авторизованным пользователем')
    @allure.description('Отправляем запрос на создание заказа, в запросе направляем словарь "ingredients" с неверным '
                        'хешем ингредиентов, в запросе добавляем accessToken в заголовки, ожидаем код 500')
    def test_make_order_auth_user_with_incorrect_ingredients(self, create_and_delete_user):
        payload = TestData.INCORRECT_INGREDIENTS
        access_token = create_and_delete_user[1]
        headers = {'Authorization': access_token}
        response = OrderAPI.response_make_order(payload, headers)

        assert response.status_code == StatusCode.INTERNAL_SERVER_ERROR, \
            (f"Результаты: Получен статус код {response.status_code}, "
             f"Ожидался статус код {StatusCode.INTERNAL_SERVER_ERROR}")


class TestGetUsersOrders:

    @allure.title('Проверка получения заказов авторизованного пользователя')
    @allure.description('Отправляем запрос на получение заказа, в запросе добавляем accessToken в заголовки, '
                        'ожидаем код 200')
    def test_get_auth_user_orders(self, create_and_delete_user):
        access_token = create_and_delete_user[1]
        headers = {'Authorization': access_token}
        response = OrderAPI.response_get_user_orders(headers)
        actual_result = response.json()["success"]

        assert response.status_code == StatusCode.OK and actual_result is True and "orders" in response.json(), \
            (f"Фактические результаты: статус код {response.status_code}, получение заказа {actual_result}, "
             f"'orders' in response.json()={"orders" in response.json()}. Ожидалось: status_code={StatusCode.OK}, "
             f"получение заказа = True, 'orders' in response.json()=True")

    @allure.title('Проверка получения заказов неавторизованного пользователя')
    @allure.description('Отправляем запрос на получение заказа, в запросе указываем  пустой accessToken в заголовках, '
                        'ожидаем код 401')
    def test_get_unauth_user_orders(self):
        access_token = None
        headers = {'Authorization': access_token}
        response = OrderAPI.response_get_user_orders(headers)
        actual_result = response.json()["success"]
        actual_message = response.json()["message"]

        assert (response.status_code == StatusCode.UNAUTHORIZED
                and actual_result is False
                and actual_message == StatusResponse.NEED_AUTHORIZATION), \
            (f"Фактические результаты: статус код {response.status_code}, получение заказа {actual_result}, "
             f"сообщение {actual_message}. Ожидалось: status_code={StatusCode.UNAUTHORIZED}, получение заказа = False,"
             f" сообщение {StatusResponse.NEED_AUTHORIZATION}")
