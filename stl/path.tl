# TechLang STL - Path Utilities
# Convenience wrappers around core path_* commands.

package name stl.path

def join a b
    path_join a b _stl_path_joined
    return _stl_path_joined
end

def basename p
    path_basename p _stl_path_base
    return _stl_path_base
end

def dirname p
    path_dirname p _stl_path_dir
    return _stl_path_dir
end

def extname p
    path_extname p _stl_path_ext
    return _stl_path_ext
end

export join
export basename
export dirname
export extname
