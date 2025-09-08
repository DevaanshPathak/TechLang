print "== Memory Demo =="
mem_alloc 3
mem_write 1 42
mem_write 2 7
mem_read 1
mem_dump
mem_free 2
mem_dump

