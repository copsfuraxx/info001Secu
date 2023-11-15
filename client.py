import socket
import ssl

def verify_certificate(cert_string, hostname):
    # Obtain the peer certificate
    cert = ssock.getpeercert()

    # Extract the subject and verify it matches the expected hostname
    subject = dict(x[0] for x in cert['subject'])
    common_name = subject.get('commonName', '')
    
    if common_name == hostname:
        print("Certificate verification successful. Domain matches.")
        return True
    else:
        print(f"Certificate verification failed. Expected: {hostname}, Actual: {common_name}")
        return False

if __name__ == '__main__':
    hostname = input('Adresse du serveur : ')
    # PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('certificates/root-ca-lorne.pem')

    with socket.create_connection((hostname, 8888)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            ssock.do_handshake()
            if verify_certificate(ssock, hostname):
                msg = input("Message : ")
                ssock.sendall(msg.encode(encoding='UTF-8',errors='strict'))
            ssock.close()
    