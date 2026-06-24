import docker
import time
import sys
import os

client = docker.from_env()

def create_network():
    network_name = "microservice-net"
    try:
        networks = client.networks.list(names=[network_name])
        if networks:
            print(f"Сеть уже существует: {network_name}")
            return networks[0]
        network = client.networks.create(network_name, driver="bridge")
        print(f"Сеть создана: {network_name}")
        return network
    except docker.errors.APIError as e:
        print(f"Ошибка создания сети: {e}")
        sys.exit(1)

def run_service_a(network_name="microservice-net"):
    try:
        container = client.containers.get("service_a")
        container.stop()
        container.remove()
        print("Старый service_a удален")
    except docker.errors.NotFound:
        pass
    
    current_dir = os.getcwd()
    service_a_path = os.path.join(current_dir, "service_a")
    
    app_path = os.path.join(service_a_path, "app.py")
    if not os.path.exists(app_path):
        print(f"ОШИБКА: Файл {app_path} не найден!")
        print("Создайте файл service_a/app.py")
        sys.exit(1)
    
    print(f"Монтируем: {service_a_path} -> /app")
    
    print("Запуск Service A...")
    return client.containers.run(
        "python:3.9-slim",
        command="sh -c 'pip install Flask -q && python /app/app.py'",
        volumes={
            service_a_path: {'bind': '/app', 'mode': 'ro'}
        },
        working_dir="/app",
        ports={'5000/tcp': 5000},
        network=network_name,
        name="service_a",
        detach=True
    )

def run_service_b(network_name="microservice-net"):
    try:
        container = client.containers.get("service_b")
        container.stop()
        container.remove()
        print("Старый service_b удален")
    except docker.errors.NotFound:
        pass
    
    current_dir = os.getcwd()
    service_b_path = os.path.join(current_dir, "service_b")
    
    app_path = os.path.join(service_b_path, "app.py")
    if not os.path.exists(app_path):
        print(f"ОШИБКА: Файл {app_path} не найден!")
        print("Создайте файл service_b/app.py")
        sys.exit(1)
    
    print(f"Монтируем: {service_b_path} -> /app")
    
    print("Запуск Service B...")
    return client.containers.run(
        "python:3.9-slim",
        command="sh -c 'pip install Flask requests -q && python /app/app.py'",
        volumes={
            service_b_path: {'bind': '/app', 'mode': 'ro'}
        },
        working_dir="/app",
        ports={'5001/tcp': 5001},
        network=network_name,
        name="service_b",
        detach=True
    )

def cleanup():
    print("\nОчистка...")
    for name in ["service_a", "service_b"]:
        try:
            container = client.containers.get(name)
            container.stop()
            container.remove()
            print(f"  ✖ {name} остановлен и удален")
        except docker.errors.NotFound:
            pass
    
    try:
        network = client.networks.get("microservice-net")
        network.remove()
        print("  ✖ сеть удалена")
    except docker.errors.NotFound:
        pass

if __name__ == "__main__":
    print("=" * 50)
    print("Запуск микросервисов")
    print("=" * 50)
    
    try:
        client.ping()
        print("Docker работает")
    except:
        print("Docker не запущен!")
        sys.exit(1)
    
    cleanup()
    
    network = create_network()
    
    service_a = run_service_a()
    print("Ожидание запуска Service A (10 секунд)...")
    time.sleep(10)
    
    service_b = run_service_b()
    print("Ожидание запуска Service B (5 секунд)...")
    time.sleep(5)
    
    print("\nСервисы запущены!")
    print("=" * 50)
    print("Проверьте работу по адресам:")
    print("http://localhost:5000/hello")
    print("http://localhost:5001/greet")
    print("=" * 50)
    print("Нажмите Ctrl+C для остановки...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()
        print("\nСервисы остановлены. До свидания!")