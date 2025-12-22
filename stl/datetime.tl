# TechLang STL - Date/Time Utilities
# Utilities built on core now/format_date and sys_time.

package name stl.datetime

def now_iso
    # Return current UTC ISO-8601 timestamp as a string.
    now _stl_dt_now
    return _stl_dt_now
end

def unix_now
    # Return current unix timestamp (seconds).
    sys_time _stl_dt_unix
    return _stl_dt_unix
end

def format_unix ts fmt
    # Return formatted unix timestamp (UTC).
    # fmt may be quoted or a string variable name.
    format_date ts fmt _stl_dt_formatted
    return _stl_dt_formatted
end

def is_iso8601 s
    # Basic ISO-8601-ish validation (shape check).
    # Accepts e.g. 2025-12-22T12:34:56+00:00
    set _stl_dt_ok 0

    str_length s _stl_dt_len
    if _stl_dt_len < 10
        return _stl_dt_ok
    end

    str_contains s "T" _stl_dt_has_t
    if _stl_dt_has_t == 0
        return _stl_dt_ok
    end

    # Accept either 'Z' or an offset like '+00:00'
    str_contains s "Z" _stl_dt_has_z
    str_contains s "+" _stl_dt_has_plus
    if _stl_dt_has_z == 0
        if _stl_dt_has_plus == 0
            return _stl_dt_ok
        end
    end

    set _stl_dt_ok 1
    return _stl_dt_ok
end

def parse_iso_parts iso
    # Extract ISO timestamp parts.
    # Returns: year month day hour min sec ok
    call is_iso8601 iso _stl_dt_is_ok
    if _stl_dt_is_ok == 0
        str_create _stl_dt_y ""
        str_create _stl_dt_m ""
        str_create _stl_dt_d ""
        str_create _stl_dt_h ""
        str_create _stl_dt_min ""
        str_create _stl_dt_s ""
        return _stl_dt_y _stl_dt_m _stl_dt_d _stl_dt_h _stl_dt_min _stl_dt_s 0
    end

    # YYYY-MM-DDTHH:MM:SS...
    str_substring iso 0 4 _stl_dt_y
    str_substring iso 5 7 _stl_dt_m
    str_substring iso 8 10 _stl_dt_d
    str_substring iso 11 13 _stl_dt_h
    str_substring iso 14 16 _stl_dt_min
    str_substring iso 17 19 _stl_dt_s

    return _stl_dt_y _stl_dt_m _stl_dt_d _stl_dt_h _stl_dt_min _stl_dt_s 1
end

export now_iso
export unix_now
export format_unix
export is_iso8601
export parse_iso_parts
