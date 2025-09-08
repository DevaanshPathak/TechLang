import math
import random
from typing import List
from .core import InterpreterState


class MathOpsHandler:
    """Advanced math functions and constants for TechLang."""

    @staticmethod
    def _get_int(state: InterpreterState, token: str) -> int:
        try:
            return int(token)
        except ValueError:
            val = state.get_variable(token, None)
            if isinstance(val, int):
                return val
            raise ValueError(f"Expected number, got '{token}'")

    @staticmethod
    def handle_math_sin(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_sin requires an angle (degrees)")
            return 0
        angle = MathOpsHandler._get_int(state, tokens[index + 1])
        rad = math.radians(angle)
        state.add_output(str(math.sin(rad)))
        return 1

    @staticmethod
    def handle_math_cos(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_cos requires an angle (degrees)")
            return 0
        angle = MathOpsHandler._get_int(state, tokens[index + 1])
        rad = math.radians(angle)
        state.add_output(str(math.cos(rad)))
        return 1

    @staticmethod
    def handle_math_sqrt(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_sqrt requires a number")
            return 0
        n = MathOpsHandler._get_int(state, tokens[index + 1])
        if n < 0:
            state.add_error("Cannot sqrt negative numbers")
            return 1
        state.add_output(str(int(math.isqrt(n))))
        return 1

    @staticmethod
    def handle_math_pow(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("math_pow requires base and exponent")
            return 0
        base = MathOpsHandler._get_int(state, tokens[index + 1])
        exp = MathOpsHandler._get_int(state, tokens[index + 2])
        state.add_output(str(int(pow(base, exp))))
        return 2

    @staticmethod
    def handle_math_random(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("math_random requires min and max")
            return 0
        lo = MathOpsHandler._get_int(state, tokens[index + 1])
        hi = MathOpsHandler._get_int(state, tokens[index + 2])
        if lo > hi:
            lo, hi = hi, lo
        state.add_output(str(random.randint(lo, hi)))
        return 2

    @staticmethod
    def handle_math_pi(state: InterpreterState) -> None:
        state.add_output(str(math.pi))

    @staticmethod
    def handle_math_e(state: InterpreterState) -> None:
        state.add_output(str(math.e))


