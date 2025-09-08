print "== Network Demo =="

# HTTP demo (requires 'requests' installed and internet access)
http_get "https://httpbin.org/status/200" resp
http_status resp

http_post "https://httpbin.org/post" "hello"
print response_status

# Server stubs
server_start 8080
server_route "/api" handler
server_stop

