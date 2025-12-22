# TechLang STL - Network Utilities
# Convenience wrappers over core http_* commands

package name stl.net

# Note: Avoids dynamic variable name construction.
# Functions either operate on fixed core names or use fixed internal response names.

def get url resp_name
    # Wrapper for http_get
    # Args: url (quoted), resp_name (string var name)
    http_get url resp_name
    return
end

def get_text url
    # GET a URL and return (body, status)
    # Returns: body (string), status (number)
    str_create _stl_net_resp ""
    set _stl_net_status 0
    try
        http_get url _stl_net_resp
        set _stl_net_status _stl_net_resp_status
    catch
        str_create _stl_net_resp ""
        set _stl_net_status 0
    end
    return _stl_net_resp _stl_net_status
end

def get_json url target_dict
    # GET a URL and parse JSON into target_dict
    # Returns: status (number)
    str_create _stl_net_resp ""
    set _stl_net_status 0
    try
        http_get url _stl_net_resp
        set _stl_net_status _stl_net_resp_status
        json_parse _stl_net_resp target_dict
    catch
        set _stl_net_status 0
    end
    return _stl_net_status
end

def post_text url data_token
    # POST data to URL and return (body, status)
    # data_token may be a string var, quoted string literal, or numeric var
    str_create _stl_net_post_resp ""
    set _stl_net_status 0
    try
        http_post url data_token
        str_create _stl_net_post_resp ""
        str_concat _stl_net_post_resp response
        set _stl_net_status response_status
    catch
        str_create _stl_net_post_resp ""
        set _stl_net_status 0
    end
    return _stl_net_post_resp _stl_net_status
end

export get
export get_text
export get_json
export post_text
