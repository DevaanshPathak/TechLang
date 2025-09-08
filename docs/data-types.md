# Data Types in TechLang

TechLang provides a variety of built-in data types to support different kinds of data and operations. Understanding these types is essential for writing effective programs.

## Primitive Types

- **Integer (`int`)**: Whole numbers, e.g., `42`, `-7`
- **Float (`float`)**: Decimal numbers, e.g., `3.14`, `-0.001`
- **Boolean (`bool`)**: Logical values, `true` or `false`
- **String (`string`)**: Text data, e.g., `"hello world"`

## Composite Types

- **Array**: Ordered collection of elements of the same type.
  ```techlang
  let numbers = [1, 2, 3, 4]
  ```
- **Tuple**: Fixed-size collection of elements of possibly different types.
  ```techlang
  let point = (3, 4)
  ```
- **Map**: Key-value pairs, similar to dictionaries.
  ```techlang
  let capitals = { "France": "Paris", "Japan": "Tokyo" }
  ```

## Special Types

- **Null (`null`)**: Represents the absence of a value.
- **Any (`any`)**: Can hold a value of any type.

## Type Inference and Annotations

TechLang can infer types, but you can also specify them:

```techlang
let age: int = 30
let name: string = "Alice"
```

## Type Conversion

Convert between types using built-in functions:

```techlang
let n = int("42")      // String to int
let s = string(3.14)   // Float to string
```

---

See the [Examples Index](examples.md) for