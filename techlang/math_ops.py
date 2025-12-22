import math
import random
from datetime import datetime, timezone
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
    def _get_float(state: InterpreterState, token: str) -> float:
        try:
            return float(token)
        except ValueError:
            val = state.get_variable(token, None)
            if isinstance(val, (int, float)):
                return float(val)
            raise ValueError(f"Expected numeric value, got '{token}'")

    @staticmethod
    def handle_math_sin(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_sin requires an angle (degrees)")
            return 0
        angle = MathOpsHandler._get_float(state, tokens[index + 1])
        rad = math.radians(angle)
        state.add_output(str(math.sin(rad)))
        return 1

    @staticmethod
    def handle_math_cos(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_cos requires an angle (degrees)")
            return 0
        angle = MathOpsHandler._get_float(state, tokens[index + 1])
        rad = math.radians(angle)
        state.add_output(str(math.cos(rad)))
        return 1

    @staticmethod
    def handle_math_tan(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_tan requires an angle (degrees)")
            return 0
        angle = MathOpsHandler._get_float(state, tokens[index + 1])
        rad = math.radians(angle)
        state.add_output(str(math.tan(rad)))
        return 1

    @staticmethod
    def handle_math_asin(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_asin requires a value between -1 and 1")
            return 0
        value = MathOpsHandler._get_float(state, tokens[index + 1])
        if not -1.0 <= value <= 1.0:
            state.add_error("math_asin domain is [-1, 1]")
            return 1
        state.add_output(str(math.degrees(math.asin(value))))
        return 1

    @staticmethod
    def handle_math_acos(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_acos requires a value between -1 and 1")
            return 0
        value = MathOpsHandler._get_float(state, tokens[index + 1])
        if not -1.0 <= value <= 1.0:
            state.add_error("math_acos domain is [-1, 1]")
            return 1
        state.add_output(str(math.degrees(math.acos(value))))
        return 1

    @staticmethod
    def handle_math_atan(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_atan requires a numeric value")
            return 0
        value = MathOpsHandler._get_float(state, tokens[index + 1])
        state.add_output(str(math.degrees(math.atan(value))))
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
    def handle_math_mod(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 2 >= len(tokens):
            state.add_error("math_mod requires dividend and divisor")
            return 0
        dividend = MathOpsHandler._get_int(state, tokens[index + 1])
        divisor = MathOpsHandler._get_int(state, tokens[index + 2])
        if divisor == 0:
            state.add_error("Cannot compute modulo by zero")
            return 2
        result = dividend % divisor
        # Store result back in the dividend variable
        var_name = tokens[index + 1]
        state.variables[var_name] = result
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
        result = int(random.randint(lo, hi))

        # Optional store form: math_random <min> <max> <targetVar>
        if index + 3 < len(tokens):
            target = tokens[index + 3]
            from .basic_commands import BasicCommandHandler

            if not (target.startswith('"') and target.endswith('"')) and target not in BasicCommandHandler.KNOWN_COMMANDS:
                state.variables[target] = result
                return 3

        state.add_output(str(result))
        return 2

    @staticmethod
    def handle_math_seed(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_seed requires a number")
            return 0
        try:
            seed_value = MathOpsHandler._get_int(state, tokens[index + 1])
        except ValueError:
            state.add_error("math_seed expects a numeric seed")
            return 0
        random.seed(seed_value)
        return 1

    @staticmethod
    def handle_math_round(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_round requires a numeric value")
            return 0
        value = MathOpsHandler._get_float(state, tokens[index + 1])
        state.add_output(str(int(round(value))))
        return 1

    @staticmethod
    def handle_math_floor(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_floor requires a numeric value")
            return 0
        value = MathOpsHandler._get_float(state, tokens[index + 1])
        state.add_output(str(math.floor(value)))
        return 1

    @staticmethod
    def handle_math_ceil(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_ceil requires a numeric value")
            return 0
        value = MathOpsHandler._get_float(state, tokens[index + 1])
        state.add_output(str(math.ceil(value)))
        return 1

    @staticmethod
    def handle_math_deg2rad(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_deg2rad requires an angle in degrees")
            return 0
        angle = MathOpsHandler._get_float(state, tokens[index + 1])
        state.add_output(str(math.radians(angle)))
        return 1

    @staticmethod
    def handle_math_rad2deg(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("math_rad2deg requires an angle in radians")
            return 0
        angle = MathOpsHandler._get_float(state, tokens[index + 1])
        state.add_output(str(math.degrees(angle)))
        return 1

    @staticmethod
    def handle_math_pi(state: InterpreterState) -> None:
        state.add_output(str(math.pi))

    @staticmethod
    def handle_math_e(state: InterpreterState) -> None:
        state.add_output(str(math.e))

    @staticmethod
    def handle_now(state: InterpreterState, tokens: List[str], index: int) -> int:
        value = datetime.now(timezone.utc).isoformat()

        # Optional store form: now <targetStr>
        if index + 1 < len(tokens):
            target = tokens[index + 1]
            from .basic_commands import BasicCommandHandler

            if not (target.startswith('"') and target.endswith('"')) and target not in BasicCommandHandler.KNOWN_COMMANDS:
                state.strings[target] = value
                return 1

        state.add_output(value)
        return 0

    @staticmethod
    def handle_format_date(state: InterpreterState, tokens: List[str], index: int) -> int:
        if index + 1 >= len(tokens):
            state.add_error("format_date requires at least a timestamp in seconds")
            return 0
        try:
            timestamp = MathOpsHandler._get_float(state, tokens[index + 1])
        except ValueError:
            state.add_error("format_date timestamp must be numeric or a numeric variable")
            return 0

        fmt = "%Y-%m-%d %H:%M:%S"
        consumed = 1
        if index + 2 < len(tokens):
            fmt_token = tokens[index + 2]
            if fmt_token.startswith('"') and fmt_token.endswith('"'):
                fmt = fmt_token[1:-1]
                consumed = 2
            elif fmt_token in state.strings:
                fmt = state.strings[fmt_token]
                consumed = 2
        try:
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            state.add_error("format_date timestamp out of range")
            return consumed

        try:
            formatted = dt.strftime(fmt)
        except ValueError as exc:
            state.add_error(f"Invalid format string: {exc}")
            return consumed

        # Optional store form:
        # - format_date <ts> <targetStr>
        # - format_date <ts> "fmt" <targetStr>
        # - format_date <ts> fmt_var <targetStr>
        target_index = index + 1 + consumed
        if target_index < len(tokens):
            candidate = tokens[target_index]
            from .basic_commands import BasicCommandHandler

            if not (candidate.startswith('"') and candidate.endswith('"')) and candidate not in BasicCommandHandler.KNOWN_COMMANDS:
                state.strings[candidate] = formatted
                return consumed + 1

        state.add_output(formatted)
        return consumed


