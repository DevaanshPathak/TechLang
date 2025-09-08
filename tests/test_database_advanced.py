from techlang.interpreter import run


def test_transactions_and_introspection(tmp_path):
    db = tmp_path / "adv.db"
    code = f"""
    db_connect "{db}"
    db_execute "CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)"
    db_begin
    db_insert t "1, Alice"
    db_rollback
    db_tables
    db_schema t
    db_indexes t
    db_disconnect
    """
    out = run(code).strip().splitlines()
    # Should list table 't'
    assert 't' in out

