# auth_locust.py
from locust import HttpUser, task, between
import random

class AuthenticatedUser(HttpUser):
    """Пользователь с аутентификацией через JWT токен"""
    wait_time = between(1, 3)
    
    def on_start(self):
        """
        Метод on_start выполняется при запуске каждого виртуального пользователя.
        Здесь происходит логин и получение токена.
        """
        # Выбираем случайного пользователя (50% user1, 50% author1)
        username = random.choice(["user1", "author1"])
        password = "pass123"
        
        # Отправляем запрос на логин
        with self.client.post("/login", json={
            "username": username,
            "password": password
        }, catch_response=True) as response:
            
            if response.status_code == 200:
                data = response.json()
                self.token = data["token"]
                self.role = data["role"]
                print(f"✓ Пользователь {username} вошел как {self.role}")
                response.success()
            else:
                self.token = None
                print(f"✗ Ошибка логина для {username}: {response.status_code}")
                response.failure(f"Login failed: {response.status_code}")
    
    @task(5)
    def view_posts(self):
        """Просмотр списка постов (требуется токен)"""
        headers = {"Authorization": f"Bearer {self.token}"} if hasattr(self, 'token') and self.token else {}
        
        with self.client.get("/posts", headers=headers, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Ошибка: {response.status_code}")
    
    @task(3)
    def view_post(self):
        """Просмотр конкретного поста (требуется токен)"""
        post_id = random.randint(1, 3)
        headers = {"Authorization": f"Bearer {self.token}"} if hasattr(self, 'token') and self.token else {}
        
        with self.client.get(f"/posts/{post_id}", headers=headers, catch_response=True) as response:
            if response.status_code == 404:
                response.failure("Пост не найден")
            elif response.status_code != 200:
                response.failure(f"Ошибка: {response.status_code}")
    
    @task(2)
    def protected_endpoint(self):
        """Доступ к защищенному эндпоинту"""
        if not hasattr(self, 'token') or not self.token:
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        with self.client.get("/protected", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                # Проверяем, что вернулся корректный ответ
                data = response.json()
                if "message" in data:
                    response.success()
                else:
                    response.failure("Неверный формат ответа")
            elif response.status_code == 401:
                response.failure("Токен недействителен или истек")
            else:
                response.failure(f"Ошибка: {response.status_code}")
    
    @task(1)
    def create_post(self):
        """
        Создание нового поста (требуется токен)
        Только авторы могут создавать посты
        """
        if not hasattr(self, 'token') or not self.token:
            return
        
        # Только авторы создают посты
        if hasattr(self, 'role') and self.role != "author":
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {
            "title": f"Пост с аутентификацией {random.randint(100, 999)}",
            "content": "Содержимое поста, созданного аутентифицированным пользователем"
        }
        
        with self.client.post("/posts", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code != 201:
                response.failure(f"Ошибка создания: {response.status_code}")
            else:
                data = response.json()
                if "id" not in data:
                    response.failure("Ответ не содержит id")
    
    @task(1)
    def home_page(self):
        """Главная страница (не требует аутентификации)"""
        self.client.get("/")