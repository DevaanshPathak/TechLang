from techlang.interpreter import run


def test_struct_create_and_print():
    code = """
    struct Person name:string age:int end
    struct new Person p1
    struct set p1 name "Ada"
    struct set p1 age 37
    struct get p1 name
    struct get p1 age
    print p1
    """
    output = run(code).strip().splitlines()
    assert output[0] == "Struct 'p1' of type 'Person' created"
    assert "Ada" in output
    assert "37" in output
    assert output[-1] == 'Person{name: "Ada", age: 37}'


def test_struct_type_checking():
    code = """
    struct Person name:string age:int end
    struct new Person p1
    struct set p1 age "oops"
    """
    output = run(code).strip()
    assert "Value '" in output and "valid integer" in output


def test_struct_debug_snapshot():
    code = """
    struct Person name:string age:int end
    struct new Person p1
    struct set p1 age 42
    debug
    """
    output = run(code).strip().splitlines()
    assert any(line.startswith("Structs:") and "p1" in line for line in output)
