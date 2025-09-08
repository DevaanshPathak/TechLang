import os
from techlang.interpreter import run


def test_file_write_and_read(tmp_path):
    d = tmp_path
    code = f"""
    file_write "{d}/a.txt" "Hello"
    file_read "{d}/a.txt" content
    print content
    """
    out = run(code, base_dir=str(d)).strip().splitlines()
    assert out[-1] == "Hello"


def test_file_append(tmp_path):
    d = tmp_path
    code = f"""
    file_write "{d}/b.txt" "Hi"
    file_append "{d}/b.txt" "!"
    file_read "{d}/b.txt" s
    print s
    """
    out = run(code, base_dir=str(d)).strip().splitlines()
    assert out[-1] == "Hi!"


def test_file_exists_and_delete(tmp_path):
    d = tmp_path
    code = f"""
    file_exists "{d}/c.txt"
    file_write "{d}/c.txt" "x"
    file_exists "{d}/c.txt"
    file_delete "{d}/c.txt"
    file_exists "{d}/c.txt"
    """
    out = run(code, base_dir=str(d)).strip().splitlines()
    # Expect: false, wrote msg (maybe), true, deleted msg (maybe), false -> ensure last is false
    assert out[-1] == "false"


def test_file_list(tmp_path):
    d = tmp_path
    os.makedirs(d/"sub", exist_ok=True)
    (d/"sub"/"x.txt").write_text("ok", encoding="utf-8")
    code = f"""
    file_list "{d}/sub"
    """
    out = run(code).strip().splitlines()
    assert "x.txt" in out

