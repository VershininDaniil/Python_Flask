import unittest
from hw1_registration import app


class TestRegistration(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_email_validation(self):
        # Корректный email
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Successfully registered", response.data.decode())

        # Некорректный email (отсутствует @)
        response = self.client.post("/registration", data={
            "email": "testexample.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data.decode())

    def test_phone_validation(self):
        # Корректный телефон (10 цифр)
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 200)

        # Телефон не 10 цифр
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 123456789,
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.data.decode())

        # Телефон отрицательный
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": -1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.data.decode())

        # Телефон пустой
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": "",
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.data.decode())

    def test_name_validation(self):
        # Корректное имя
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 200)

        # Пустое имя
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data.decode())

    def test_address_validation(self):
        # Корректный адрес
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 200)

        # Пустой адрес
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "",
            "index": 123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("address", response.data.decode())

    def test_index_validation(self):
        # Корректный индекс
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 200)

        # Отрицательный индекс
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": -123456
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("index", response.data.decode())

        # Пустой индекс
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("index", response.data.decode())

    def test_comment_optional(self):
        # Без комментария
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(response.status_code, 200)

        # С комментарием
        response = self.client.post("/registration", data={
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "Иван",
            "address": "Москва",
            "index": 123456,
            "comment": "Привет"
        })
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()