from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import socket
import datetime
import json

app = Flask(__name__, static_folder='static')

# Маршрут для index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message.html', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        try:
            send_to_socket(username, message)
            return render_template('message.html', success=True)
        except Exception as e:
            print(f"Error sending message: {e}")
            return render_template('message.html', success=False)
    return render_template('message.html')

# Маршрут для помилки 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

# Функція для відправки даних на сокет-сервер
def send_to_socket(username, message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('socket', 5000))
        data = {
            'username': username,
            'message': message,
            'date': str(datetime.datetime.now())
        }
        sock.sendall(json.dumps(data).encode())
    except Exception as e:
        print(f"Error sending data to socket: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
