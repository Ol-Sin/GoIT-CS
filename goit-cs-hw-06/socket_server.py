import socket
import pymongo
import json
from datetime import datetime

# Підключення до MongoDB
client = pymongo.MongoClient('mongodb://mongodb:27017/')
db = client['message_database']
collection = db['messages']

def start_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 5000))
    sock.listen(1)
    print("Socket server listening on port 5000...")

    while True:
        connection, address = sock.accept()
        print(f"Connection accepted from {address}")  # Додаємо лог для підтвердження
        try:
            data = connection.recv(1024)
            if data:
                message_data = json.loads(data.decode())
                print(f"Received data: {message_data}")  # Лог для відстеження даних
                save_to_mongo(message_data)
        finally:
            connection.close()

def save_to_mongo(message_data):
    try:
        message_data['date'] = datetime.now().isoformat()
        collection.insert_one(message_data)
        print(f"Message saved to MongoDB: {message_data}")
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")

if __name__ == '__main__':
    start_socket_server()
