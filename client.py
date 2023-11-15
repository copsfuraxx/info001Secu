import socket
import ssl
import fnmatch

def verify_certificate(cert_string, hostname):
    # Obtain the peer certificate
    cert = ssock.getpeercert()

    san_entries = [entry[1] for entry in cert.get('subjectAltName', []) if entry[0] == 'DNS']
    
    if any(fnmatch.fnmatchcase(hostname, entry) for entry in san_entries):
        print("Certificate verification successful. Domain matches.")
        return True
    else:
        print(f"Certificate verification failed.")
        return False

if __name__ == '__main__':
    hostname = input('Adresse du serveur : ')
    # PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # context.load_verify_locations('certificates/root-ca-lorne.pem')
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 8888)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            ssock.do_handshake()
            # if verify_certificate(ssock, hostname):
            msg = input("Message : ")
            ssock.sendall(msg.encode(encoding='UTF-8',errors='strict'))
            ssock.close()
    