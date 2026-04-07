import json
import logging
import unittest

from remote_execution import app



# Настройка конфигурации логгирования
logging.basicConfig(level=logging.DEBUG)


class RemoteExecution(unittest.TestCase):
    code = ''
    timeout = None

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    def test_timeout(self):
        """Тайм-аут ниже, чем время исполнения."""

        client = self.app
        response = client.post('/run_code', json = {
            'code': 'print("Hello, World!")',
            'timeout': 0.0002
        }
                               )
        self.assertEqual(response.status_code, 200)
        logging.debug('Response status code: %s', response.status_code)

        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Время вышло!')
        logging.debug('Response data: %s', data)


    def test_invalid_input(self):
        """Некорректно введённые данные в форме."""

        client = self.app
        response = client.post(
            '/run_code', json = {
                'code': '',
                'timeout': 31
            }
        )
        self.assertEqual(response.status_code, 400)
        logging.debug('Response status code: %s', response.status_code)

        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Некорректный ввод данных!')
        logging.debug('Response data: %s', data)

    def test_unsafe_input(self):
        """Небезопасный ввод в поле с кодом."""

        client = self.app
        response = client.post(
            '/run_code', json = {
                'code': 'import os; os.system("echo unsafe")',
                'timeout': 3
            }
        )
        self.assertEqual(response.status_code, 400)
        logging.debug('Response status code %s', response.status_code)

        data = json.loads(response.data)
        self.assertIn('output', data)
        if data['output'] is not None:
            self.assertIn('unsafe', data['output'])
            logging.debug('Response data: %s', data)

        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Небезопасный код!')
        logging.debug('Response data %s', data)


if __name__ == '__main__':
    unittest.main()