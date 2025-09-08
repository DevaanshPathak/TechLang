import pytest
from techlang.interpreter import run


class TestWhileLoops:
    """Test while loop functionality in TechLang"""
    
    def test_simple_while_loop(self):
        """Test a basic while loop that counts down"""
        code = """
        set x 3
        while x > 0
            print x
            sub x 1
        end
        """
        output = run(code).strip().splitlines()
        assert output == ["3", "2", "1"]
    
    def test_while_loop_with_condition_false_initially(self):
        """Test while loop that doesn't execute because condition is false initially"""
        code = """
        set x 0
        while x > 5
            print x
            add x 1
        end
        print "Done"
        """
        output = run(code).strip().splitlines()
        assert output == ["Done"]
    
    def test_while_loop_sum_numbers(self):
        """Test while loop that sums numbers from 1 to 5"""
        code = """
        set sum 0
        set i 1
        while i <= 5
            add sum i
            add i 1
        end
        print sum
        """
        output = run(code).strip()
        assert output == "15"  # 1+2+3+4+5 = 15
    
    def test_while_loop_factorial(self):
        """Test while loop that calculates factorial"""
        code = """
        set n 4
        set factorial 1
        while n > 0
            mul factorial n
            sub n 1
        end
        print factorial
        """
        output = run(code).strip()
        assert output == "24"  # 4! = 4*3*2*1 = 24
    
    def test_while_loop_with_array(self):
        """Test while loop that fills an array"""
        code = """
        array_create numbers 3
        set i 0
        while i < 3
            array_set numbers i i
            add i 1
        end
        array_get numbers 0
        array_get numbers 1
        array_get numbers 2
        """
        output = run(code).strip().splitlines()
        # The output includes the array creation message, so we check the last 3 lines
        assert output[-3:] == ["0", "1", "2"]
    
    def test_while_loop_invalid_syntax(self):
        """Test while loop with invalid syntax"""
        code = "while x"
        output = run(code).strip()
        assert "Invalid 'while' command" in output
    
    def test_while_loop_invalid_condition(self):
        """Test while loop with invalid condition value"""
        code = """
        while x > abc
            print x
        end
        """
        output = run(code).strip()
        assert "Expected a number or variable for comparison" in output
    
    def test_while_loop_non_numeric_variable(self):
        """Test while loop with non-numeric variable"""
        code = """
        set x "hello"
        while x > 0
            print x
        end
        """
        output = run(code).strip()
        assert "Expected a number for variable" in output
    
    def test_while_loop_nested_with_if(self):
        """Test while loop with nested if statement"""
        code = """
        set x 3
        while x > 0
            if x > 1
                print "High"
            end
            sub x 1
        end
        """
        output = run(code).strip().splitlines()
        assert output == ["High", "High"]  # x=3 and x=2 are > 1
    
    def test_while_loop_with_string_operations(self):
        """Test while loop with string operations"""
        code = """
        str_create message "Hello"
        set i 0
        while i < 3
            str_concat message "!"
            add i 1
        end
        print message
        """
        output = run(code).strip()
        assert output == "Hello!!!"
    
    def test_while_loop_infinite_prevention(self):
        """Test that while loop doesn't run forever with reasonable limit"""
        code = """
        set x 1
        set count 0
        while x > 0
            add count 1
            if count > 5
                set x 0
            end
        end
        print count
        """
        # This test ensures the while loop can be controlled
        output = run(code).strip()
        assert output == "6"  # Should count to 6 then exit
