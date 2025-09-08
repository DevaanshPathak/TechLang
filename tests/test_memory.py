from techlang.interpreter import run


def test_memory_alloc_write_read_and_free():
    code = """
    mem_alloc 2
    mem_write 1 10
    mem_read 1
    mem_free 1
    mem_read 1
    """
    out = run(code).strip().splitlines()
    # After write, reading returns 10
    assert out[0] == "1" or out[0].isdigit()  # base address printed (1 in current model)
    assert out[1] == "10"
    # After free, reading should error
    assert any("not allocated" in line for line in out[2:])


def test_memory_dump():
    code = """
    mem_alloc 3
    mem_write 1 5
    mem_dump
    """
    out = run(code).strip().splitlines()
    assert any(": 5" in line for line in out)

