# TechLang STL - JSON Utilities
# Thin wrappers over core json_* commands

package name stl.json

def parse source target
    # Wrapper for json_parse
    # Args: source (string var name or quoted JSON), target (dict/array/string/var target name)
    json_parse source target
    return
end

def stringify source target_str
    # Wrapper for json_stringify
    # Args: source (dict/array/string/var name), target_str (string var name)
    json_stringify source target_str
    return
end

def read path target
    # Wrapper for json_read
    # Args: path (quoted), target (target name)
    json_read path target
    return
end

def write source path
    # Wrapper for json_write
    # Args: source (dict/array name), path (quoted)
    json_write source path
    return
end

def try_parse source target
    # Attempt json_parse, returning 1 on success else 0
    # Returns: ok (number)
    set _stl_json_ok 1
    try
        json_parse source target
    catch
        set _stl_json_ok 0
    end
    return _stl_json_ok
end

export parse
export stringify
export read
export write
export try_parse
