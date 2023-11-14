import requests

if __name__ == '__main__':
    r = requests.get('http://localhost:8000/api/')
    while True:
        r = requests.post('http://localhost:8000/api/msg', json={'msg' : input("Enter your message: ")})