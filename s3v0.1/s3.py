#!/usr/bin/env python3

import os
import sys

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    interpreter_path = os.path.join(script_dir, "interpreter.py")

    if not os.path.exists(interpreter_path):
        print("Error: interpreter.py not found in the same directory as the script.", file=sys.stderr)
        exit(1)

    # Run the interpreter with the given program as argument
    os.execlp("python3", "python3", interpreter_path, *sys.argv[1:]) # replace os.system with os.execlp

if __name__ == "__main__":
    main()