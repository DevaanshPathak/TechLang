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


def test_thread_status_result_and_list():
    code = """
    def worker
        thread_sleep 50
        print "done"
    end
    thread_create worker
    thread_status 1
    thread_result 1
    thread_list
    thread_join 1
    thread_status 1
    thread_result 1
    thread_list
    """
    out = run(code).splitlines()
    # First line is the thread id from thread_create
    assert out[0] == '1'
    # Depending on timing, status may already be finished; accept both states
    assert out[1] in {"running", "finished"}
    # Result before completion should be empty unless the thread already finished
    assert out[2] in {"", "done"}
    # thread_list should include the thread id
    assert out[3] == "1"
    # thread_join output should include the worker's print
    assert "done" in out[4]
    # After join, status must be finished and result cached
    assert out[5] == "finished"
    assert out[6] == "done"
    assert out[7] == "1"


def test_thread_wait_all_collects_outputs():
    code = """
    def alpha
        print "alpha"
    end
    def beta
        thread_sleep 50
        print "beta"
    end
    thread_create alpha
    thread_create beta
    thread_wait_all
    """
    out = run(code).splitlines()
    assert out[0] == "1"
    assert out[1] == "2"
    # thread_wait_all should emit the outputs from both threads, order by thread id
    assert "alpha" in out[2]
    assert "beta" in out[3]


def test_mutex_and_queue_commands():
    code = """
    mutex_create lock
    mutex_lock lock
    mutex_unlock lock
    queue_push inbox "hello"
    queue_push inbox "world"
    queue_pop inbox message
    print message
    queue_pop inbox message
    print message
    """
    out = run(code).splitlines()
    assert out[0] == "created"
    assert out[1] == "locked"
    assert out[2] == "unlocked"
    # Queue pops should allow printing retrieved messages
    assert out[3] == "hello"
    assert out[4] == "world"

