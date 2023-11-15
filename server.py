import socket
import ssl
import threading

def job(conn, addr):
    data = conn.recv(1024)
    if not data:
        conn.close()
        return
    
    print(data.decode(encoding='UTF-8',errors='strict'))
    conn.close()

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('certificates/serveur_http.cert.pem', 'certificates/serveur_http.pem')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('localhost', 8888))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()
            t = threading.Thread(target=job, args=(conn,addr,))
            t.start()