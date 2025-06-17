# Wudge interpreter
Wudge is a minimalist esoteric programming language with only 6 commands focused on string manipulation and basic control flow. It operates through variable assignment, user input, conditional execution based on pattern matching, and simple jumping for loops and control structures. 

## Features
-   **Variables**: Store and retrieve values dynamically.
-   **String Editing**: Pattern replacement with support for multiple simultaneous substitutions.
-   **Conditionals**: Conditional logic that executes the next n lines if the specified pattern has been found.
-   **I/O**: Interact with the user through console input and output.
-   **Control Flow**: Jump to specific line numbers for loops and program flow control.

  
## Getting Started

### Prerequisites

-   Python 3.x

### Usage

1.  Clone or download the `wudge.py` interpreter script.
2.  Create a text file with your Wudge code (e.g., `my_program.wudge`).
3.  Run the interpreter from your terminal and provide the filename when prompted:
    ```sh
    python ampell.py
    Enter a file with valid Wudge code: my_program.wudge
    ```

---

## Examples

### 1. Hello, World!

The most simple of a program; printing a string.
```wudge
set x {Hello, world!}
print x
```
### 2. Truth-Machine

Ask user for number, repeat input forever if user inputted 1, and print 0 once if user inputted 0.
```wudge
set prompt {I need 1 or 0}
ask prompt input
if input found [1] do 2
print input
jump 4
if input found [0] do 1
print input
```

### 3. Infinite Cat program

Ask user for string, repeat string, and repeat.
```wudge
set prompt {}
ask prompt input
print input
jump 1
```

## Wudge Syntax Guide

| Command                        | Description                                                       |
|-------------------------------|-------------------------------------------------------------------|
| `set a {b}`                   | Set variable `a` to value `b`                                     |
| `ask a b`                     | Ask `a` as the prompt and get user's input stored in variable `b` |
| `jump 10`                     | Jump to line 10                                                   |
| `print a`                     | Print value of variable `a`                                       |
| `replace a [b/c],[d/e] to f`  | Replace patterns `b` with `c` and `d` with `e` in `a`, append to `f` |
| `if a found [b] do 10`        | If pattern `b` is found in `a`, run the next 10 lines; else skip |

