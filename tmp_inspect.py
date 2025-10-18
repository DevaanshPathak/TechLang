import tempfile
import pathlib
from techlang.interpreter import run
from techlang.system_ops import ProcessOpsHandler
import techlang.data_types as data_types_module
from techlang.core import InterpreterState

print('cache before', ProcessOpsHandler._stream_cache)
script = """import time
print('tick')
time.sleep(0.1)
print('tock')
"""
with tempfile.TemporaryDirectory() as tmp:
    path = pathlib.Path(tmp) / 'slow.py'
    path.write_text(script)
    cmd = f'"python" "{path}"'
    out = run(f"proc_spawn {cmd} proc_wait 1 1.0")
    print('run output', out)
    print('cache mid', ProcessOpsHandler._stream_cache)
    print('module alias same', data_types_module.ProcessOpsHandler is ProcessOpsHandler)
    manual_state = InterpreterState()
    print('hydrate manual', ProcessOpsHandler.hydrate_stream_array(manual_state, 'proc_1_out'))
    print('manual arrays', manual_state.arrays)
    out2 = run("array_get proc_1_out 0 array_get proc_1_out 1")
    print('array run output', out2)
    print('cache end', ProcessOpsHandler._stream_cache)
