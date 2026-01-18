# myutils/math.tl - Math utilities submodule

def double x
    mul x 2
    return x
end
export double

def triple x
    mul x 3
    return x
end
export triple

def square x
    mul x x
    return x
end
export square

def add_nums a b
    set result a
    add result b
    return result
end
export add_nums
