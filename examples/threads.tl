print "== Threads Demo =="

def worker
    ping ping print
end

thread_create worker
thread_create worker
thread_sleep 200

print "Joining..."
thread_join 1
thread_join 2

