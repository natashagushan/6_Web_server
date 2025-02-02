import socket
import datetime as d
import os


def file_reader(name):
    file = open(name, 'r')
    content = file.read()
    file.close()
    return content.encode()


def image_reader(name):
    file = open(name, 'rb')
    content = file.read()
    file.close()
    return content


sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

while True:
    conn, addr = sock.accept()
    print("Connected", addr)

    data = conn.recv(8192)
    msg = data.decode()

    print(msg)

    file_name = msg.split()[1]
    path_to_file = os.path.join(os.getcwd(), file_name[1:])
    date = d.datetime.today()

    if os.path.exists(path_to_file) == True:
        if path_to_file.split('.')[1] == 'txt':
            type_of_file = 'text/html'
            conn.send(file_reader(path_to_file))
        elif path_to_file.split('.')[1] == 'html':
            type_of_file = 'text/html'
            conn.send(file_reader(path_to_file))
        elif path_to_file.split('.')[1] == 'img':
            type_of_file = 'image/jpeg'
            conn.send(image_reader(path_to_file))
        elif path_to_file.split('.')[1] == 'jpg':
            type_of_file = 'image/jpeg'
            conn.send(image_reader(path_to_file))
        elif path_to_file.split('.')[1] == 'png':
            type_of_file = 'image/jpeg'
            conn.send(image_reader(path_to_file))

    else:
        resp = """HTTP/1.1 404 Not found
    Server: SelfMadeServer v0.0.1
    Content-type: {}
    Date: {}
    Connection: close
    Charset: UTF-8
    """.format(type_of_file, date)
        conn.send(resp.encode())

conn.close()