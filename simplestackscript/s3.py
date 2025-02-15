# s3_package/s3.py
import argparse
import os
import sys
from .interpreter import Interpreter

def main():
    parser = argparse.ArgumentParser(
        description="Run an S3 script.",
        epilog="For more information, see the README or the project's GitHub page."
    )

    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s 0.2.4"
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

        if not filename.endswith(".s3"): # Check file extension
            print("Error: Unknown file extension.", file=sys.stderr)
            exit(1)

        try:
            with open(filename, "r") as f:
                code = f.read()
                interpreter = Interpreter()
                interpreter.run(code)
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