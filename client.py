import ssl
import socket
import os


def verify_certificate(cert_string, hostname):
    # Save the certificate string to a temporary file
    with open('temp_cert.crt', 'w') as cert_file:
        cert_file.write(cert_string)

    try:
        # Verify the certificate chain, expiration, and hostname using OpenSSL commands
        result_chain = subprocess.run(['openssl', 'verify', 'temp_cert.crt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_dates = subprocess.run(['openssl', 'x509', '-noout', '-dates', '-in', 'temp_cert.crt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_subject = subprocess.run(['openssl', 'x509', '-noout', '-subject', '-in', 'temp_cert.crt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check the return codes and display the results
        if result_chain.returncode != 0:
            print("Certificate chain verification failed. Error:", result_chain.stderr.decode('utf-8'))
            return False

        if result_dates.returncode != 0:
            print("Error checking certificate expiration. Error:", result_dates.stderr.decode('utf-8'))
            return False

        if result_subject.returncode == 0:
            subject = result_subject.stdout.decode('utf-8').strip()
            print("Certificate subject:", subject)
            if hostname in subject:
                print("Hostname verification successful.")
            else:
                print("Hostname verification failed. Expected:", hostname)
        else:
            print("Error checking certificate subject. Error:", result_subject.stderr.decode('utf-8'))

    finally:
        # Cleanup: Remove the temporary certificate file
        subprocess.run(['rm', 'temp_cert.crt'])

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.depoisier.fr', 9999))
    # s.connect(('localhost', 9999))
    certificat = s.recv()
    if not verify_certificate(certificat, 'www.depoisier.fr'):
        s.close()
        pass
    print(certificat)
    msg = input("Message : ")
    s.sendall(msg.encode(encoding='UTF-8',errors='strict'))
    s.close()