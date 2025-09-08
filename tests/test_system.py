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

