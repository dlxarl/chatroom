import socket
import threading

# Список для збереження підключених клієнтів та їх адрес.
clients = []

# Функція для обробки з'єднання клієнта.
def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')  # Отримати повідомлення від клієнта.
            if not message:  # Якщо повідомлення порожнє, це означає, що клієнт закрив з'єднання.
                remove_client(client_socket)
                break
            broadcast_message(message, client_socket)
        except:
            remove_client(client_socket)
            break

# Функція для відправки повідомлення всім клієнтам, окрім відправника.
def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

# Функція для видалення клієнта зі списку підключених.
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

# Функція для запуску сервера.
def start_chatroom(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Створити сокет.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Дозволити використання тієї ж адреси та порту після закриття.
    server_socket.bind((host, port))  # Зв'язати сокет з адресою та портом.
    server_socket.listen(5)  # Почати слухати з'єднання на вказаному порті.
    print(f"Сервер запущений на {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()  # Прийняти вхідне з'єднання клієнта.
        print(f"З'єднано з {address[0]}:{address[1]}")

        clients.append(client_socket)  # Додати клієнта до списку підключених.

        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()  # Запустити потік для обробки з'єднання з клієнтом.

if __name__ == "__main__":
    host = '127.0.0.1'  # Встановити тут свою IP-адресу або '0.0.0.0', щоб прослуховувати всіх клієнтів.
    port = 139  # Встановити тут бажаний порт для чат-руму.
    start_chatroom(host, port)  # Запустити сервер чат-руму.