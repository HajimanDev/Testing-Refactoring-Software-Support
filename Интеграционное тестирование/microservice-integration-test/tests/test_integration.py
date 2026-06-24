import requests

def test_greet_service_b():
    response = requests.get('http://localhost:5001/greet')
    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "Hello from Service A"
    print("Тест пройден!")

if __name__ == "__main__":
    test_greet_service_b()