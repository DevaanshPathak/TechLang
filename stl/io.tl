# TechLang STL - I/O Utilities
# Convenience wrappers around file_* commands using silent/store forms.

package name stl.io

def read_text path
    # Read file.
    # Returns: text ok
    try
        file_read path _stl_io_text
    catch
        str_create _stl_io_empty ""
        return _stl_io_empty 0
    end
    return _stl_io_text 1
end

def write_text path text
    # Write text to file (silent).
    # Returns: ok
    file_write path text _stl_io_ok
    return _stl_io_ok
end

def append_text path text
    # Append text to file (silent).
    # Returns: ok
    file_append path text _stl_io_ok
    return _stl_io_ok
end

def delete path
    # Delete file (silent).
    # Returns: ok
    file_delete path _stl_io_ok
    return _stl_io_ok
end

def exists path
    # Returns: 1/0
    file_exists path _stl_io_exists
    return _stl_io_exists
end

def listdir path outArr
    # Store entries into outArr.
    # Returns: ok
    file_list path outArr _stl_io_ok
    return _stl_io_ok
end

export read_text
export write_text
export append_text
export delete
export exists
export listdir
