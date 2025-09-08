from techlang.interpreter import run


def test_http_status_missing():
    out = run("http_status resp").strip()
    assert "No status for 'resp'" in out


def test_server_stubs():
    out = run("server_start 8080 server_route \"/x\" h server_stop").strip().splitlines()
    assert "Server started" in out[0]
    assert "Route registered" in out[1]
    assert "Server stopped" in out[2]

