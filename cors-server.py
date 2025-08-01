from http.server import SimpleHTTPRequestHandler, HTTPServer

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()


if __name__ == '__main__':
    PORT = 8080
    server = HTTPServer(('0.0.0.0', PORT), CORSRequestHandler)
    print(f"Serving with CORS at http://localhost:{PORT}")
    server.serve_forever()