from __future__ import annotations

import re
import tempfile
from pathlib import Path

from techlang.interpreter import run


def test_stl_datetime_now_iso_is_iso8601(base_dir: str):
    code = """
    package use stl/datetime
    call stl.datetime.now_iso ts
    call stl.datetime.is_iso8601 ts ok
    print ok
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["1"]


def test_stl_datetime_format_unix_epoch(base_dir: str):
    code = """
    package use stl/datetime
    call stl.datetime.format_unix 0 "%Y-%m-%d" out
    print out
    """
    output = run(code, base_dir=base_dir).strip()
    assert output == "1970-01-01"


def test_stl_datetime_parse_iso_parts(base_dir: str):
    code = """
    package use stl/datetime
    str_create iso "2025-12-22T12:34:56+00:00"
    call stl.datetime.parse_iso_parts iso y m d hh mm ss ok
    print y
    print m
    print d
    print hh
    print mm
    print ss
    print ok
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["2025", "12", "22", "12", "34", "56", "1"]


def test_stl_random_seeded_randint_sequence(base_dir: str):
    code = """
    package use stl/random
    call stl.random.seed 123 seeded
    call stl.random.randint 1 10 a
    call stl.random.randint 1 10 b
    call stl.random.randint 1 10 c
    call stl.random.randint 1 10 d
    call stl.random.randint 1 10 e
    print seeded
    print a
    print b
    print c
    print d
    print e
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["1", "1", "5", "2", "7", "5"]


def test_stl_random_choice_seeded(base_dir: str):
    code = """
    package use stl/random
    array_create arr
    array_push arr 10
    array_push arr 20
    array_push arr 30
    call stl.random.seed 123 seeded
    call stl.random.choice arr val ok
    print val
    print ok
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["10", "1"]


def test_stl_random_shuffle_seeded(base_dir: str):
    code = """
    package use stl/random
    array_create arr
    array_push arr 1
    array_push arr 2
    array_push arr 3
    array_push arr 4
    call stl.random.seed 123 seeded
    call stl.random.shuffle arr out
    array_get out 0 a
    array_get out 1 b
    array_get out 2 c
    array_get out 3 d
    print a
    print b
    print c
    print d
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["3", "4", "2", "1"]


def test_stl_path_ops(base_dir: str):
    code = """
    package use stl/path
    call stl.path.join "dir" "file.txt" p
    call stl.path.basename p b
    call stl.path.dirname p d
    call stl.path.extname p e
    print b
    print d
    print e
    """
    output = run(code, base_dir=base_dir).strip().splitlines()
    assert output == ["file.txt", "dir", ".txt"]


def test_stl_io_roundtrip(base_dir: str):
    project_root = Path(base_dir)

    with tempfile.TemporaryDirectory(dir=project_root) as tmp:
        tmp_dir = Path(tmp)
        rel_dir = tmp_dir.relative_to(project_root).as_posix()
        file_rel = f"{rel_dir}/hello.txt"

        code = f'''
        package use stl/io
        call stl.io.write_text "{file_rel}" "hello" ok1
        call stl.io.exists "{file_rel}" ex1
        call stl.io.read_text "{file_rel}" txt1 ok2
        call stl.io.append_text "{file_rel}" " world" ok3
        call stl.io.read_text "{file_rel}" txt2 ok4
        call stl.io.delete "{file_rel}" ok5
        call stl.io.exists "{file_rel}" ex2
        print ok1
        print ex1
        print txt1
        print ok2
        print ok3
        print txt2
        print ok4
        print ok5
        print ex2
        '''

        output = run(code, base_dir=base_dir).strip().splitlines()

    assert output[0] == "1"
    assert output[1] == "1"
    assert output[2] == "hello"
    assert output[3] == "1"
    assert output[4] == "1"
    assert output[5] == "hello world"
    assert output[6] == "1"
    assert output[7] == "1"
    assert output[8] == "0"


def test_stl_datetime_unix_now_is_intish(base_dir: str):
    code = """
    package use stl/datetime
    call stl.datetime.unix_now ts
    print ts
    """
    output = run(code, base_dir=base_dir).strip()
    assert re.fullmatch(r"\d+", output)
