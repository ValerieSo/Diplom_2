import allure
import pytest
from data.data import StatusCode, StatusResponse, TestData
from base_api_methods import UserAPI
from data.helpers import Generators


class TestCreateUser:
    @allure.title('Проверка создания нового пользователя')
    @allure.description('Создаем пользователя, передав все валидные параметры, ожидаем код 200')
    def test_create_user_with_valid_regdata_ok(self, registration_user_data):
        payload = registration_user_data
        response = UserAPI.response_create_user(payload)
        actual_result = response.json()["success"]
        user_data = response.json()["user"]["email"]

        assert (response.status_code == StatusCode.OK
                and actual_result is True
                and user_data == payload["email"]), \
            (f"Фактические результаты:  статус код {response.status_code}, пользователь создан {actual_result}, "
             f" email пользователя {user_data}. Ожидалось: статус код {StatusCode.OK}, пользователь создан=True, "
             f"email пользователя {payload['email']}")
        # удаляем тестового пользователя
        access_token = response.json()['accessToken']
        headers = {'Authorization': access_token}
        UserAPI.delete_user(headers)

    @allure.title('Проверка создания пользователя с параметрами уже зарегистированного пользователя')
    @allure.description('Создаем пользователя, передав все валидные параметры, снова отправляем запрос на создание '
                        'пользователя с этими данными, ожидаем код 403')
    def test_create_user_with_existing_user_params_forbidden(self, registration_user_data):
        payload = registration_user_data
        response_1 = UserAPI.response_create_user(payload)
        response_2 = UserAPI.response_create_user(payload)
        actual_result = response_2.json()["success"]
        actual_message = response_2.json()["message"]

        assert (response_2.status_code == StatusCode.FORBIDDEN
                and actual_result is False
                and actual_message == StatusResponse.USER_ALREADY_EXISTS), \
            (f"Фактические результаты: статус код - {response_2.status_code}, пользователь создан - {actual_result}, "
             f"сообщение - {actual_message}. Ожидалось: статус код - {StatusCode.FORBIDDEN},"
             f"создание пользователя - False, ожидаемое сообщение - {StatusResponse.USER_ALREADY_EXISTS}")
        # удаляем тестового пользователя
        access_token = response_1.json()['accessToken']
        headers = {'Authorization': access_token}
        UserAPI.delete_user(headers)

    @allure.title('Проверка создания пользователя без отправки обязательных параметров')
    @allure.description('Отправляем три запроса на создание пользователя, с помощью параметризации почередно '
                        'убираем из запроса параметры "email", "password", "name", в каждом случае ожидаем код 403')
    @pytest.mark.parametrize('user_reg_data', [
        Generators.registration_user_data_without_email(),
        Generators.registration_user_data_without_password(),
        Generators.registration_user_data_without_name()])
    def test_create_user_without_required_params_forbidden(self, user_reg_data):
        payload = user_reg_data
        response = UserAPI.response_create_user(payload)
        actual_result = response.json()["success"]
        actual_message = response.json()["message"]

        assert (response.status_code == StatusCode.FORBIDDEN
                and actual_result is False
                and actual_message == StatusResponse.NOT_ENOUGH_DATA), \
            (f"Фактические результаты: статус код - {response.status_code}, пользователь создан - {actual_result}, "
             f"сообщение - {actual_message}. Ожидалось: статус код - {StatusCode.FORBIDDEN},"
             f"создание пользователя - False, ожидаемое сообщение - {StatusResponse.NOT_ENOUGH_DATA}")


class TestLoginUser:
    @allure.title('Проверка авторизации пользователя, при указании всех обязательных полей')
    @allure.description('Совершаем авторизацию, используя тестовые данные в payload, ожидаем код 200')
    def test_login_user_with_existing_data_ok(self, create_and_delete_user):
        payload = create_and_delete_user[0]
        response = UserAPI.response_login_user(payload)
        actual_result = response.json()["success"]
        user_data = response.json()["user"]["email"]

        assert (response.status_code == StatusCode.OK
                and actual_result is True
                and user_data == payload["email"]), \
            (f"Фактические результаты:  статус код {response.status_code}, пользователь авторизован {actual_result}, "
             f" email пользователя {user_data}. Ожидалось: статус код {StatusCode.OK}, пользователь авторизован=True, "
             f"email пользователя {payload['email']}")

    @allure.title('Проверка авторизации пользователя, без отправки обязательных параметров')
    @allure.description('Отправляем два запроса на аторизацию пользователя, с помощью параметризации почередно '
                        ' в одном запросе убираем параметр "email", во втором "password", '
                        'в каждом случае ожидаем код 401')
    @pytest.mark.parametrize('login_data', [TestData.TEST_LOGIN_PAYLOAD_INVALID_EMAIL,
                                            TestData.TEST_LOGIN_PAYLOAD_INVALID_PWD],)
    def test_login_user_without_required_params_unauthorized(self, login_data):
        payload = login_data
        response = UserAPI.response_login_user(payload)
        actual_result = response.json()["success"]
        actual_message = response.json()["message"]

        assert (response.status_code == StatusCode.UNAUTHORIZED
                and actual_result is False
                and actual_message == StatusResponse.LOGIN_FAILED), \
            (f"Фактические результаты: статус код - {response.status_code}, пользователь авторизован - {actual_result},"
             f"сообщение - {actual_message}. Ожидалось: статус код - {StatusCode.UNAUTHORIZED},"
             f"пользователь авторизован - False, ожидаемое сообщение - {StatusResponse.LOGIN_FAILED}")


class TestChangeUserInfo:
    @allure.title('Проверка изменения поля "email" существующего  авторизированного пользователя ')
    @allure.description('Создаем пользователя, добавляем accessToken в заголовки, '
                        'отправляем запрос на изменение поля "email", ожидаем код  200')
    def test_change_user_email_ok(self, create_and_delete_user):
        payload = create_and_delete_user[0]
        payload["email"] = Generators.generate_random_email()
        access_token = create_and_delete_user[1]
        headers = {'Authorization': access_token}
        response = UserAPI.response_change_user_info(payload, headers)
        actual_result = response.json()["success"]
        new_data = response.json()['user']['email']

        assert (response.status_code == StatusCode.OK
                and actual_result is True
                and new_data == payload["email"]), \
            (f"Фактические результаты:  статус код {response.status_code}, изменения выполнены {actual_result}, "
             f" email пользователя {new_data}. Ожидалось: статус код {StatusCode.OK}, изменения выполнены - True, "
             f"email пользователя {payload['email']}")

    @allure.title('Проверка изменения поля "email" существующего  авторизированного пользователя на email '
                  'другого существующего пользователя ')
    @allure.description('Создаем пользователя, добавляем accessToken в заголовки, отправляем запрос на изменение '
                        'поля "email",передав email другого существующего пользователя, ожидаем код  403')
    def test_change_user_email_to_existing_email_forbidden(self, create_and_delete_user):
        payload = create_and_delete_user[0]
        payload["email"] = TestData.EXISTING_EMAIL
        access_token = create_and_delete_user[1]
        headers = {'Authorization': access_token}
        response = UserAPI.response_change_user_info(payload, headers)
        actual_result = response.json()["success"]
        actual_message = response.json()['message']

        assert (response.status_code == StatusCode.FORBIDDEN
                and actual_result is False
                and actual_message == StatusResponse.EMAIL_TAKEN),  \
            (f"Фактические результаты: статус код - {response.status_code}, изменения выполнены  - {actual_result},"
             f"сообщение - {actual_message}. Ожидалось: статус код - {StatusCode.FORBIDDEN},"
             f"изменения выполнены - False, ожидаемое сообщение - {StatusResponse.EMAIL_TAKEN}")

    @allure.title('Проверка изменения поля "password" существующего  авторизированного пользователя ')
    @allure.description('Создаем пользователя, добавляем accessToken в заголовки, '
                        'отправляем запрос на изменение поля "password", ожидаем код  200')
    def test_change_user_password(self, create_and_delete_user):
        payload = create_and_delete_user[0]
        payload["password"] = Generators.generate_random_password()
        access_token = create_and_delete_user[1]
        headers = {'Authorization': access_token}
        response = UserAPI.response_change_user_info(payload, headers)
        actual_result = response.json()["success"]

        assert (response.status_code == StatusCode.OK and actual_result is True),  \
            (f"Фактические результаты:  статус код {response.status_code}, изменения выполнены {actual_result}, "
             f"Ожидалось: статус код {StatusCode.OK}, изменения выполнены - True")

    @allure.title('Проверка изменения поля "name" существующего  авторизированного пользователя ')
    @allure.description('Создаем пользователя, добавляем accessToken в заголовки, '
                        'отправляем запрос на изменение поля "name", ожидаем код  200')
    def test_change_user_name(self, create_and_delete_user):
        payload = create_and_delete_user[0]
        payload["name"] = Generators.generate_random_name()
        access_token = create_and_delete_user[1]
        headers = {'Authorization': access_token}
        response = UserAPI.response_change_user_info(payload, headers)
        actual_result = response.json()["success"]
        new_data = response.json()['user']['name']

        assert (response.status_code == StatusCode.OK
                and actual_result is True
                and new_data == payload["name"]),  \
            (f"Фактические результаты:  статус код {response.status_code}, изменения выполнены {actual_result}, "
             f" name пользователя {new_data}. Ожидалось: статус код {StatusCode.OK}, изменения выполнены - True, "
             f"name пользователя {payload['email']}")

    @allure.title('Проверка изменения поля "email" существующего  неавторизированного пользователя')
    @allure.description('Создаем пользователя, отправляем запрос на изменение поля "email", ожидаем код  401')
    def test_change_unauth_user_email_ok(self, create_and_delete_user):
        payload = create_and_delete_user[0]
        payload["email"] = Generators.generate_random_email()
        access_token = None
        headers = {'Authorization': access_token}
        response = UserAPI.response_change_user_info(payload, headers)
        actual_result = response.json()["success"]
        actual_message = response.json()['message']

        assert (response.status_code == StatusCode.UNAUTHORIZED
                and actual_result is False
                and actual_message == StatusResponse.NEED_AUTHORIZATION), \
            (f"Фактические результаты: статус код - {response.status_code}, изменения выполнены  - {actual_result},"
             f"сообщение - {actual_message}. Ожидалось: статус код - {StatusCode.UNAUTHORIZED},"
             f"изменения выполнены - False, ожидаемое сообщение - {StatusResponse.NEED_AUTHORIZATION}")

    @allure.title('Проверка изменения поля "password" существующего  неавторизированного пользователя ')
    @allure.description('Создаем пользователя, отправляем запрос на изменение поля "password", ожидаем код  401')
    def test_change_unauth_user_password_ok(self, create_and_delete_user):
        payload = create_and_delete_user[0]
        payload["password"] = Generators.generate_random_password()
        access_token = None
        headers = {'Authorization': access_token}
        response = UserAPI.response_change_user_info(payload, headers)
        actual_result = response.json()["success"]
        actual_message = response.json()['message']

        assert (response.status_code == StatusCode.UNAUTHORIZED
                and actual_result is False
                and actual_message == StatusResponse.NEED_AUTHORIZATION), \
            (f"Фактические результаты: статус код - {response.status_code}, изменения выполнены  - {actual_result},"
             f"сообщение - {actual_message}. Ожидалось: статус код - {StatusCode.UNAUTHORIZED},"
             f"изменения выполнены - False, ожидаемое сообщение - {StatusResponse.NEED_AUTHORIZATION}")

    @allure.title('Проверка изменения поля "name" существующего  неавторизированного пользователя ')
    @allure.description('Создаем пользователя, отправляем запрос на изменение поля "name", ожидаем код  401')
    def test_change_unauth_user_name_ok(self, create_and_delete_user):
        payload = create_and_delete_user[0]
        payload["name"] = Generators.generate_random_name()
        access_token = None
        headers = {'Authorization': access_token}
        response = UserAPI.response_change_user_info(payload, headers)
        actual_result = response.json()["success"]
        actual_message = response.json()['message']

        assert (response.status_code == StatusCode.UNAUTHORIZED
                and actual_result is False
                and actual_message == StatusResponse.NEED_AUTHORIZATION), \
            (f"Фактические результаты: статус код - {response.status_code}, изменения выполнены  - {actual_result},"
             f"сообщение - {actual_message}. Ожидалось: статус код - {StatusCode.UNAUTHORIZED},"
             f"изменения выполнены - False, ожидаемое сообщение - {StatusResponse.NEED_AUTHORIZATION}")
