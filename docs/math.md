# Math & Date Utilities in TechLang

TechLang ships a collection of stack-friendly commands for scientific math, numeric formatting, and basic date/time handling. All commands emit their result through `InterpreterState.add_output`, so they can be composed with other language features.

## Randomness & Constants

```techlang
math_random 1 6        # integer in [1,6]
math_pi                # prints π as a float
math_e                 # prints Euler's constant
```

`math_random` accepts either literal numbers or numeric variables. If the lower bound is greater than the upper bound the arguments are swapped automatically.

## Trigonometry (Degrees In, Floats Out)

The trigonometric helpers expect degree input and return floats. Inverse functions emit degrees to keep composition intuitive.

```techlang
math_sin 90            # 1.0
math_cos 0             # 1.0
math_tan 45            # 0.9999999999999999
math_asin 1            # 90.0
math_acos 0            # 90.0
math_atan 1            # 45.0
math_deg2rad 180       # 3.141592653589793
math_rad2deg 1.5708    # 89.999... (degrees)
```

All arguments can come from numeric variables. Domain checks guard `math_asin` and `math_acos`; values outside `[-1, 1]` emit descriptive errors that match the wording in `tests/test_math_ops.py`.

## Roots, Powers, and Rounding

```techlang
math_sqrt 144          # 12 (integer square root)
math_pow 2 10          # 1024
math_round 3.55        # 4
math_floor 3.55        # 3
math_ceil 3.01         # 4
```

`math_sqrt` mirrors the interpreter's integer-first design by using floor square roots. For fractional support prefer `math_pow` with exponent `0.5`.

## Date & Time Helpers

```techlang
now                    # 2025-10-23T12:34:56.789123+00:00 (UTC ISO8601)
format_date 1700000000 "%Y-%m-%d"   # 2023-11-14
```

- `now` captures the current UTC time using `datetime.now(timezone.utc)` and always returns an ISO 8601 string with offset.
- `format_date <seconds>` interprets the argument as Unix seconds (can be float) and formats it in UTC. Supply an optional quoted `strftime` pattern; invalid timestamps and formats emit `[Error: ...]` messages consumed by tests.

## Error Handling

- Invalid domains (e.g. `math_asin 2`) call `state.add_error("math_asin domain is [-1, 1]")` so tests can assert the exact copy.
- Missing arguments (e.g. `math_round`) yield specific `requires` errors mirroring other math commands.
- `format_date` returns `timestamp out of range` or `Invalid format string` depending on the failure source.

See `tests/test_math_ops.py` for ready-made assertions and `examples/data_types_demo.tl` for integration patterns.