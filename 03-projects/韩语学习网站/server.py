"""HTTP server with audio download + Range request support for seeking."""
import http.server
import subprocess
import urllib.parse
import os, re, json, mimetypes

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/download"):
            return self.handle_download()
        return self.serve_file()

    def serve_file(self):
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            self.send_error(404)
            return

        ctype, _ = mimetypes.guess_type(path)
        fsize = os.path.getsize(path)

        # Handle Range requests (required for audio seeking)
        range_header = self.headers.get('Range')
        if range_header and fsize > 0:
            try:
                m = re.match(r'bytes=(\d+)-(\d*)', range_header)
                if m:
                    start = int(m.group(1))
                    end = int(m.group(2)) if m.group(2) else fsize - 1
                    if start >= fsize:
                        self.send_response(416)
                        self.end_headers()
                        return
                    end = min(end, fsize - 1)
                    self.send_response(206)
                    self.send_header('Content-Range', f'bytes {start}-{end}/{fsize}')
                    self.send_header('Accept-Ranges', 'bytes')
                    self.send_header('Content-Type', ctype or 'audio/mp4')
                    self.send_header('Content-Length', str(end - start + 1))
                    self.end_headers()
                    with open(path, 'rb') as f:
                        f.seek(start)
                        self.wfile.write(f.read(end - start + 1))
                    return
            except Exception:
                pass

        self.send_response(200)
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Type', ctype or 'audio/mp4')
        self.send_header('Content-Length', str(fsize))
        self.end_headers()
        with open(path, 'rb') as f:
            self.wfile.write(f.read())

    def handle_download(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        url = params.get("url", [""])[0]
        if not url:
            return self.send_json({"error": "Missing url"}, 400)

        m = re.search(r'[?&]v=([\w-]+)', url)
        if not m:
            return self.send_json({"error": "Bad URL"}, 400)

        vid = m.group(1)
        output_path = os.path.join(AUDIO_DIR, f"{vid}.m4a")
        if os.path.exists(output_path):
            return self.send_json({"file": output_path, "status": "ready"})

        try:
            result = subprocess.run(
                ["yt-dlp", "-f", "bestaudio[ext=m4a]", "-o", output_path, url],
                capture_output=True, text=True, timeout=120
            )
            if os.path.exists(output_path):
                return self.send_json({"file": output_path, "status": "ready"})
            return self.send_json({"error": "Download failed"}, 500)
        except subprocess.TimeoutExpired:
            return self.send_json({"error": "Timeout"}, 500)
        except Exception as e:
            return self.send_json({"error": str(e)}, 500)

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    port = 8766
    print(f"Server: http://localhost:{port}")
    http.server.HTTPServer(("", port), Handler).serve_forever()
