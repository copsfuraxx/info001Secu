import socket

def verify_certificate(cert_string, hostname):
    pass

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect(('www.depoisier.fr', 9999))
    s.connect(('localhost', 9999))
    certificat = s.recv(4096)
    if not verify_certificate(certificat, 'www.depoisier.fr'):
        s.close()
        pass
    print(certificat)
    msg = input("Message : ")
    s.sendall(msg.encode(encoding='UTF-8',errors='strict'))
    s.close()