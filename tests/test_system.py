import os
import sys
from techlang.interpreter import run


def test_sys_env_time_date():
    out = run("sys_env PATH sys_time sys_date").strip().splitlines()
    assert len(out) >= 2


def test_sys_exec_echo():
    cmd = '"python" -c "print(123)"'
    out = run(f"sys_exec {cmd}").strip().splitlines()
    assert any("123" in line for line in out)


def test_proc_spawn_and_wait():
    cmd = '"python" -c "print(456)"'
    out = run(f"proc_spawn {cmd} proc_wait 1").strip().splitlines()
    # First line is pid '1'
    assert out[0] == '1'
    assert any("456" in line for line in out[1:])


def test_sys_sleep_and_cwd():
    out = run("sys_cwd").strip()
    assert out == os.getcwd()
    # sys_sleep should not emit output but should not error either
    assert run("sys_sleep 5").strip() == ""


def test_proc_status_reports_running_then_exit():
    cmd = '"python" -c "import time; time.sleep(0.1)"'
    out = run(f"proc_spawn {cmd} proc_status 1 sys_sleep 200 proc_status 1").strip().splitlines()
    assert out[0] == '1'
    assert out[1] == 'running'
    # After waiting, process should have exited with status 0
    assert out[2] == '0'


def test_proc_wait_timeout_and_stream_arrays(tmp_path):
    script = tmp_path / "slow.py"
    script.write_text("""import time
print('tick')
time.sleep(0.2)
print('tock')
""")
    cmd = f'"python" "{script}"'
    code = f"proc_spawn {cmd} proc_wait 1 1.0"
    out = run(code)
    lines = out.strip().splitlines()
    assert lines[0] == '1'
    # Wait output should include tick/tock
    assert 'tick' in lines[1]
    assert 'tock' in lines[2]
    # Arrays should retain individual lines
    result = run("array_get proc_1_out 0 array_get proc_1_out 1")
    arr_lines = result.strip().splitlines()
    assert 'tick' in arr_lines[0]
    assert 'tock' in arr_lines[1]


def test_proc_wait_timeout_triggers_error():
    cmd = '"python" -c "import time; time.sleep(0.5)"'
    out = run(f"proc_spawn {cmd} proc_wait 1 0.1").strip().splitlines()
    assert out[0] == '1'
    assert any('timeout' in line.lower() for line in out[1:])

