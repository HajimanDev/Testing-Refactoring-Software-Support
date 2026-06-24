# locustfile.py (полная версия с двумя классами)
from locust import HttpUser, task, between
import random

class Reader(HttpUser):
    """Пользователи-читатели (80% от общего числа)"""
    weight = 4
    wait_time = between(0.5, 2)
    
    def on_start(self):
        print(f"Читатель {self} начал работу")
    
    @task(5)
    def view_posts(self):
        with self.client.get("/posts", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Ошибка: {response.status_code}")
            else:
                if not isinstance(response.json(), list):
                    response.failure("Ответ не является списком")
    
    @task(3)
    def view_post(self):
        post_id = random.randint(1, 3)
        with self.client.get(f"/posts/{post_id}", catch_response=True) as response:
            if response.status_code == 404:
                response.failure("Пост не найден")
            elif response.status_code != 200:
                response.failure(f"Ошибка: {response.status_code}")
    
    @task(1)
    def home_page(self):
        self.client.get("/")

class Author(HttpUser):
    """Пользователи-авторы (20% от общего числа)"""
    weight = 1
    wait_time = between(0.5, 2)
    
    def on_start(self):
        print(f"Автор {self} начал работу")
    
    @task(3)
    def view_posts(self):
        with self.client.get("/posts", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Ошибка: {response.status_code}")
    
    @task(2)
    def view_post(self):
        post_id = random.randint(1, 3)
        with self.client.get(f"/posts/{post_id}", catch_response=True) as response:
            if response.status_code == 404:
                response.failure("Пост не найден")
    
    @task(2)
    def create_post(self):
        payload = {
            "title": f"Авторский пост {random.randint(100, 999)}",
            "content": "Содержимое нового поста от автора"
        }
        with self.client.post("/posts", json=payload, catch_response=True) as response:
            if response.status_code != 201:
                response.failure(f"Ошибка создания: {response.status_code}")
    
    @task(1)
    def home_page(self):
        self.client.get("/")