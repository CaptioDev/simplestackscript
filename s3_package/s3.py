#!/usr/bin/env python3

import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Run an S3 script.",
        epilog="For more information, see the README or the project's GitHub page or on PyPI."
    )

    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s 0.2.10"
    )

    parser.add_argument("filename", nargs="?", help="The S3 script file to execute (optional).")

    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    interpreter_path = os.path.join(script_dir, "interpreter.py")

    if not os.path.exists(interpreter_path):
        print("Error: interpreter.py not found in the same directory as the script.", file=sys.stderr)
        exit(1)

    if args.filename:
        filename = args.filename
        try:
            # Run the interpreter with the given program as argument
            os.execlp("python3", "python3", interpreter_path, filename)  # Pass filename directly
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.", file=sys.stderr)  # Print to stderr
            exit(1) # Exit with an error code
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)  # Print to stderr
            exit(1) # Exit with an error code

    else:
        parser.print_help()

if __name__ == "__main__":
    main()