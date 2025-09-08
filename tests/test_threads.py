from techlang.interpreter import run


def test_thread_create_and_join():
    code = """
    def job
        ping ping print
    end
    thread_create job
    thread_create job
    thread_sleep 100
    thread_join 1
    thread_join 2
    """
    out = run(code).strip().splitlines()
    # First two lines are thread ids '1' and '2'
    assert out[0] == '1'
    assert out[1] == '2'
    # Joins should print the outputs from those jobs; each job prints '2'
    assert '2' in out[-2]
    assert '2' in out[-1]

