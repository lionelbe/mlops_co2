import requests
import datetime
import os
import json

def api_url():
    return 'http://mlops-app:8000'

def save_test_results(results):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"test_results_{current_datetime}.txt"
    folder_path = "log"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w") as file:
        file.write(results)
    print(f"Test results saved to {filename}")

def run_tests():
    results = []

    def assert_test(condition, success_message, expected_response=None, actual_response=None):
        if condition:
            results.append(success_message)
        else:
            error_message = f"Assertion failed! Expected: {expected_response}, Actual: {actual_response}"
            if actual_response is not None:
                error_message += f"\nActual status code: {actual_response.status_code}"
            results.append(error_message)

    def test_status(api_url):
        header = "Test: Status Endpoint"
        results.append(f"\n=== {header} ===")
        response = requests.get(f"{api_url}/status")
        expected_response = {'message': 'API is running!'}
        assert_test(response.status_code == 200, "Status endpoint returned 200", expected_response, response.json())
        results.append(f"Response: {json.dumps(response.json(), indent=4)}")

    def test_create_user(api_url):
        header = "Test: User Creation Endpoint"
        results.append(f"\n=== {header} ===")
        response = requests.post(f"{api_url}/users", json={"username": "testuser", "password": "testpassword"})
        expected_response = {'message': 'User created successfully'}
        assert_test(response.status_code == 200, "User creation endpoint returned 200", expected_response, response.json())
        results.append(f"Response: {json.dumps(response.json(), indent=4)}")

    def test_login(api_url):
        header = "Test: Login Endpoint"
        results.append(f"\n=== {header} ===")
        response = requests.post(f"{api_url}/login", json={"username": "testuser", "password": "testpassword"})
        expected_response = {'message': 'Login successful'}
        assert_test(response.status_code == 200, "Login endpoint returned 200", expected_response, response.json())
        results.append(f"Response: {json.dumps(response.json(), indent=4)}")

    def test_prediction(api_url):
        header = "Test: CO2 Emissions Prediction Endpoint"
        results.append(f"\n=== {header} ===")
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
        auth = ('testuser', 'testpassword')
        try:
            response = requests.post(f"{api_url}/predict", json=car_data, auth=auth)
            assert_test(response.status_code == 200, "Prediction endpoint returned 200", None, response.json())
        except Exception as e:
            assert_test(False, "An error occurred during the prediction request", str(e))

        results.append(f"Response: {json.dumps(response.json(), indent=4)}")

    def test_get_history(api_url):
        header = "Test: Get History Endpoint"
        results.append(f"\n=== {header} ===")
        auth = ('testuser', 'testpassword')
        try:
            response = requests.get(f"{api_url}/personal_history", auth=auth)
            assert_test(response.status_code == 200, "Get History endpoint returned 200", None, response.json())
        except Exception as e:
            assert_test(False, "An error occurred during the history request", str(e))

        results.append(f"Response: {json.dumps(response.json(), indent=4)}")

    # Run the tests
    test_status(api_url())
    test_create_user(api_url())
    test_login(api_url())
    test_prediction(api_url())
    test_get_history(api_url())
    test_results = "\n".join(results)
    save_test_results(test_results)
    print(test_results)

run_tests()
