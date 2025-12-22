import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from techlang.interpreter import run


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002 - match stdlib signature
        # Silence server logs during tests
        return

    def do_GET(self):  # noqa: N802 - stdlib naming
        if self.path == "/hello":
            body = b"hello"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/json":
            body = b'{"x":1}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):  # noqa: N802 - stdlib naming
        if self.path != "/echo":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", "0"))
        data = self.rfile.read(length) if length > 0 else b""
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


@pytest.fixture()
def local_http_base_url():
    server = HTTPServer(("127.0.0.1", 0), _Handler)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_stl_net_get_text(local_http_base_url, base_dir: str):
    pytest.importorskip("requests")
    code = f'''
    package use stl/net
    call stl.net.get_text "{local_http_base_url}/hello" body status
    print body
    print status
    '''
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["hello", "200"]


def test_stl_net_post_text(local_http_base_url, base_dir: str):
    pytest.importorskip("requests")
    code = f'''
    package use stl/net
    call stl.net.post_text "{local_http_base_url}/echo" "ping" body status
    print body
    print status
    '''
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["ping", "200"]


def test_stl_net_get_json(local_http_base_url, base_dir: str):
    pytest.importorskip("requests")
    code = f'''
    package use stl/net
    call stl.net.get_json "{local_http_base_url}/json" "obj" status
    dict_get obj "x"
    print status
    '''
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert "Parsed JSON object into dictionary 'obj'" in output[0]
    assert output[1] == "1"
    assert output[2] == "200"


def test_stl_json_parse_wrapper_array(base_dir: str):
    code = '''
    package use stl/json
    str_create data "[1,2,3]"
    call stl.json.parse data "arr"
    array_get arr 1
    '''
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert "Parsed JSON array into array 'arr'" in output[0]
    assert output[1] == "2"


def test_stl_json_stringify_wrapper_array(base_dir: str):
    code = '''
    package use stl/json
    array_create nums 3
    array_set nums 0 10
    array_set nums 1 20
    array_set nums 2 30
    call stl.json.stringify "nums" "out"
    print out
    '''
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output[-1] == "[10,20,30]"


def test_stl_json_try_parse_ok(base_dir: str):
    code = '''
    package use stl/json
    str_create data "[1,2]"
    call stl.json.try_parse data "arr" ok
    print ok
    array_get arr 0
    '''
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output[-2:] == ["1", "1"]


def test_stl_json_try_parse_invalid(base_dir: str):
    code = '''
    package use stl/json
    str_create data "not valid json"
    call stl.json.try_parse data "out" ok
    print ok
    '''
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert any(line.startswith("[Error: Invalid JSON:") for line in output)
    assert output[-1] == "0"
