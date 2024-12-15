# Install and Build

```
pip install -r requirements.txt
chmod +x build.sh
./build.sh
```

See [Python runtime targets](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) for more information.

# Simple Example

Try parsing an example:

```
python ./core/driver.py core/examples/simple.c

# Use debug mode to print syntax tree
python ./core/driver.py -D core/examples/simple.c

# Check coverted bril program
python ./core/driver.py core/examples/simple.c | bril2txt

# Run coverted bril program
python ./core/driver.py core/examples/simple.c | brili -p
```

# Test

```
chmod +x ./test_c_vs_bril.sh
./test_c_vs_bril.sh ./tests/
```

# Features

## Types

> Translate to `int`, `bool` types and `const` in bril

- primitive data types (int, bool)
- const type qualifier

## Arithmetic

> Translate to `add`, `mul`, `sub`, `div` in bril

- binary operators (+,-,*,/,%)
    - `%` is supportted through `a % b = a − (a / b) × b`
- assignment operators (+=, -=, *=, /=)
- postfix operators (++, --)
- prefix operators (++, --)
- unary - operator

## Comparison

> Translate to `eq`, `lt`, `gt`, `le`, `ge` in bril

> Notice that bril will treat the result after comparison as bool, so `int x = 3 < 5;` in C will be converted to `bool x = 3 < 5;`.

- comparison operators (<,>,=,<=,>=,==,!=)

## Logic

> Translate to `not`, `and`, `or` in bril

- boolean logic (!,&&,||)

## Control

> Translate to `jmp`, `br` and `labels` in bril

- for loops (for, continue, break)
- if statements (if-then-else)

## Functions

> Translate to `call`, `ret` in bril

- function definition
- function calls
- return statement

## I/O

> Translate to `print` in bril

- printf function
