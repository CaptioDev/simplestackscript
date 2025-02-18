# S# - Simple Stack Script 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/) [![Built with Python](https://img.shields.io/badge/Built_With-Python-blue)](https://www.python.org) [![PyPI version](https://img.shields.io/pypi/v/simplestackscript)](https://pypi.org/project/simplestackscript/) [![CodeQL](https://github.com/CaptioDev/simplestackscript/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/CaptioDev/simplestackscript/actions/workflows/github-code-scanning/codeql) [![GitHub last commit](https://img.shields.io/github/last-commit/CaptioDev/simplestackscript)](https://github.com/CaptioDev/simplestackscript/commits/main) 

S# (Simple Stack Script) is a lightweight, stack-based programming language designed for simplicity and power. It combines stack-based execution with variable support, making it an excellent choice for scripting, automation, and embedded systems.

## Important: We are now an officially published Python package!!!

## 🚀 Features

-   **Stack-Based Execution:** Operates on a Last-In-First-Out (LIFO) stack.
-   **Named Variables:** Store and retrieve values easily.
-   **Concise Syntax:** Readable and intuitive for programmers.
-   **Control Flow:** Supports conditionals and loops.
-   **Function Support:** Define and reuse stack-based functions.
-   **Minimal & Fast:** Designed for lightweight execution.
-   **Published Python Package:** You can find our package as [simplestackscript on PyPI.](https://pypi.org/project/simplestackscript/)
-   **Enhanced Error Handling:** Improved validation and debugging messages.

---

## 📥 Installation

If you are reading this on PyPI, please use the first installation choice below:

```bash
pip install simplestackscript
```

This is the easiest way to install S#.  pip will automatically download and install the latest version from PyPI.
If you would rather install from source, follow the instructions below:

1.  **Clone the repository with HTTPS:**

    ```bash
    git clone https://github.com/CaptioDev/simplestackscript.git
    cd simplestackscript
    ```

2.  **Install the interpreter:**

    ```bash
    pip install .  # Installs the s3 command
    ```

3.  **Run an S3 program:**

    ```bash
    s3 my_program.s3
    ```

> [!NOTE]
> You can also clone the repository using SSH and your GitHub Public Key by replacing the first line within the first step to: `git clone git@github.com:CaptioDev/simplestackscript.git`

---

## 📖 Language Reference

S# uses a stack-based architecture, where most operations manipulate a stack of values.  Instructions are processed sequentially.

### Stack Manipulation

*   **`PUSH <number>`:** Pushes the given `<number>` onto the top of the stack.
*   **`POP`:** Removes the top element from the stack.
*   **`DUP`:** Duplicates the top element of the stack and pushes the copy onto the stack.
*   **`SWAP`:** Swaps the top two elements on the stack.
*   **`ROT`:** Rotates the top three elements of the stack.

### Arithmetic Operations

*   **`ADD`:** Pops the top two elements from the stack, adds them, and pushes the result back onto the stack.
*   **`SUB`:** Pops the top two elements (a, b) and pushes `b - a` onto the stack.
*   **`MUL`:** Pops the top two elements, multiplies them, and pushes the result.
*   **`DIV`:** Pops the top two elements (a, b) and performs integer division `b // a`, pushing the result.

### Input/Output

*   **`PRINT <string_literal>`:** Prints the given `<string_literal>` to the console.
*   **`READ`:** Reads an integer from the user's input and pushes it onto the stack.
*   **`PRINT.TOP`:** Prints the value at the top of the stack without removing it.

### Control Flow

*   **`GOTO <label>`:** Jumps to the specified `<label>`.
*   **`LOOP <label> <repeat_count>`:** Loops execution from `label` for `repeat_count` times.

### Program Termination

*   **`HALT`:** Terminates the program execution.

### Labels

*   **`<label>:`:** A label marks a specific location in the program code. Used as a target for jump instructions.

### New Instructions

*   **`WAIT <milliseconds>`:** Pauses execution for the specified number of milliseconds before proceeding.

---

## 📝 Examples

```ssharp
# Example: Adding two numbers
PUSH 5
PUSH 10
ADD
PRINT.TOP  # Output: 15
HALT

# Example: Input and output
PRINT "Enter a number:"
READ
PRINT "You entered:"
PRINT.TOP
HALT

# Example: Looping
PUSH 5
LOOP 0 3  # Loop 3 times, jumping to line 0
HALT

# Example: Using WAIT
PRINT "Waiting for 3 seconds..."
WAIT 3000
PRINT "Done!"
HALT
```

<details>
<summary>ALL FEATURE EXAMPLE</summary>

This example includes all of the different opcodes and usage! Hopefully this isn't out of date...

```sscript
PUSH 16
PRINT.TOP
POP

PUSH 2
PRINT.TOP
POP

PUSH 2
PUSH 3
ADD
PRINT.TOP
POP

PUSH 3
PUSH 2
SUB
PRINT.TOP
POP

PUSH 3
PUSH 2
MUL
PRINT.TOP
POP

PUSH 4
PUSH 2
DIV
PRINT.TOP
POP

PRINT "We are testing, bum ba dum ba dum dum daaaa!"

GOTO yes
HALT

yes:
PRINT "Yep!"

PUSH 16
DUP
PRINT.TOP
POP
PRINT.TOP
POP

PUSH 10
PUSH 12
SWAP
PRINT.TOP
POP
PRINT.TOP
POP

PUSH 1
PUSH 2
PUSH 3
ROT
PRINT.TOP
POP
PRINT.TOP
POP
PRINT.TOP
POP

READ
PRINT.TOP

GOTO test-loop

test:
PRINT "Should happen 5 times!"

test-loop:
LOOP test 5

HALT
PRINT "Nope!"
```

</details>

## 💡 Contributing

Contributions are welcome! Please open an issue or submit a pull request. If you want to email us, contact at: sapinyo@proton.me

