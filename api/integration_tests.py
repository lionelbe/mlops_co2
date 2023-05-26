import unittest
from fastapi.testclient import TestClient
from api.app import app


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_status(self):
        response = self.client.get('/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'API is running!'})

    def test_create_user(self):
        response = self.client.post('/users', json={"username": "test_user", "password": "test_password"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User created successfully"})

    def test_login(self):
        response = self.client.post('/login', json={"username": "test_user", "password": "test_password"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Login successful"})

    def test_get_equiv_table(self):
        response = self.client.get('/equiv_table/lib_mrq')
        self.assertEqual(response.status_code, 200)

    def test_predict_co2_emissions(self):
        car_data = {
            "lib_mrq": 26,
            "cod_cbr": 1,
            "hybride": 0,
            "puiss_max": 190.0,
            "typ_boite_nb_rapp": 1,
            "conso_urb": 16.5,
            "conso_exurb": 9.5,
            "conso_mixte": 12.1,
            "masse_ordma_min": 2186,
            "masse_ordma_max": 2275,
            "Carrosserie": 6,
            "gamme": 5
        }

        response = self.client.post('/predict', json=car_data)
        self.assertEqual(response.status_code, 200)

    def test_get_history(self):
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)

    def test_get_personal_history(self):
        credentials = ("test_user", "test_password")

        response_login = self.client.post('/login', auth=credentials)
        self.assertEqual(response_login.status_code, 200)

        token = response_login.json().get('access_token')
        headers = {'Authorization': f'Bearer {token}'}

        response = self.client.get('/personal_history', headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
