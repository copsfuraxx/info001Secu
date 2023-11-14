import socket
import threading

def job(conn, addr):
    with open('certificates/server_http.cert.pem', 'r') as cert_file:
        cert = cert_file.read()
    try:
        conn.sendall(cert.encode(encoding='UTF-8',errors='strict'))
    finally:
        cert_file.close()
    data = conn.recv(1024)
    if not data:
        conn.close()
        return
    
    print(data.decode(encoding='UTF-8',errors='strict'))
    conn.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 9999))
    s.listen(3)

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=job, args=(conn,addr,))
        t.start()