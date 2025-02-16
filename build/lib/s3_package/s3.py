#!/usr/bin/env python3

import argparse
import sys
import os
from simplestackscript.interpreter import Interpreter  # Import the interpreter class

def main():
    parser = argparse.ArgumentParser(
        description="Run an S3 script.",
        epilog="For more information, see the README or the project's GitHub page."
    )

    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s 0.2.6"
    )

    parser.add_argument("filename", nargs="?", help="The S3 script file to execute (optional).")

    args = parser.parse_args()


    if args.filename:
        filename = args.filename

        if not filename.endswith(".s3"):  # Check file extension
            print("Error: Filename must end with '.s3'", file=sys.stderr)
            exit(1)

        try:
            with open(filename, "r") as f:
                code = f.read()
                interpreter = Interpreter()  # Create an instance of the Interpreter class
                interpreter.run(code)  # Use the run method of the interpreter
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.", file=sys.stderr)
            exit(1)
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            exit(1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()