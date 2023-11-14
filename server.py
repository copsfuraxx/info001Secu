import json
import logging
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if re.search('/api/msg', self.path):
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length).decode('utf8')

            try:
                # Assuming data is a JSON-formatted string
                data_dict = json.loads(data)

                # Now you can access the values in the dictionary
                message = data_dict.get('msg', 'Default Message')
                print(f"Message: {message}")

                self.send_response(200)
            except json.JSONDecodeError:
                self.send_response(400)
        else:
            self.send_response(403)
        self.end_headers()

    # def do_GET(self):
    #     if re.search('/api/get/*', self.path):
    #         record_id = self.path.split('/')[-1]
    #         if record_id in LocalData.records:
    #             self.send_response(200)
    #             self.send_header('Content-Type', 'application/json')
    #             self.end_headers()

    #             # Return json, even though it came in as POST URL params
    #             data = json.dumps(LocalData.records[record_id]).encode('utf-8')
    #             logging.info("get record %s: %s", record_id, data)
    #             self.wfile.write(data)

    #         else:
    #             self.send_response(404, 'Not Found: record does not exist')
    #     else:
    #         self.send_response(403)
    #     self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), HTTPRequestHandler)
    print('Starting server')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print('Stopping server')