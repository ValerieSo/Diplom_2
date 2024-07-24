import random
import string
from faker import Faker
from base_api_methods import OrderAPI
import random as r


class Generators:
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @staticmethod
    def generate_random_email():
        fake = Faker(locale="ru_Ru")
        email = fake.email()
        return email

    @staticmethod
    def generate_random_password():
        password = Generators.generate_random_string(6)
        return password

    @staticmethod
    def generate_random_name():
        fake = Faker(locale="ru_Ru")
        name = fake.name()
        return name

    @staticmethod
    def ingredients_set():
        response = OrderAPI.response_get_ingredients()
        ingredients_data = response.json()["data"]
        buns = []
        for ingredient in ingredients_data:
            if ingredient["type"] == "bun":
                buns.append(ingredient["_id"])
        sauces = []
        for ingredient in ingredients_data:
            if ingredient["type"] == "sauce":
                sauces.append(ingredient["_id"])
        mains = []
        for ingredient in ingredients_data:
            if ingredient["type"] == "main":
                mains.append(ingredient["_id"])
        order_bun = r.choice(buns)
        order_sauce = r.choice(sauces)
        order_main = r.choice(mains)
        return {"ingredients": [order_bun, order_sauce, order_main]}