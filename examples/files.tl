print "== File Ops Demo =="
file_write "tmp_out.txt" "Hello World"
file_append "tmp_out.txt" "!"
file_exists "tmp_out.txt"
file_read "tmp_out.txt" content
print content
file_list "."
file_delete "tmp_delete_me.txt"
file_write "tmp_delete_me.txt" "bye"
file_exists "tmp_delete_me.txt"
file_delete "tmp_delete_me.txt"
file_exists "tmp_delete_me.txt"

