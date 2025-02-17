# Import libraries
import sys
from time import sleep

# Take the filepath from the argument when running this script
program_filepath = sys.argv[1]

##################################################
#                  Tokenization                  #
##################################################

# Read the file line by line
program_lines = []
with open(program_filepath, 'r') as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]

program = []                                        # Stores program tokens
token_counter = 0                                   # Stores the number of tokens
label_tracker = {}                                  # Stores the token place of labels

for line in program_lines:                          # Go through each line of the program

    line = line.split("#", 1)[0].strip()            # Remove the comments from every line
    
    if not line:                                    # Remove all empty lines
        continue

    line_parts = line.split(" ")                    # Split the line by spaces
    opcode = line_parts[0]                          # Define the opcode as the first part of the line

    if opcode.endswith(":"):
        label_tracker[opcode[:-1]] = token_counter                           # Store the label and its token number
        continue

    program.append(opcode)                                                   # Add the opcode to the program, increment the token counter
    token_counter += 1

    ##################################################
    #            Handle Paremeter Opcodes            #
    ##################################################

    if opcode == "PUSH":                                                     # ---- If the opcode is PUSH ----
        try:
            number = int(line_parts[1])                                      # Parse the number
            program.append(number)                                           # Add the number to the program
            token_counter += 1                                               # Increment the token counter

        except (IndexError, ValueError):                                     # If the number is not valid
            raise ValueError(f"Invalid number in PUSH: {line}")              # Gracefully raise a program error

    elif opcode == "PRINT":                                                  # ---- If the opcode is PRINT ----

        raw_string = ' '.join(line_parts[1:]).strip()                        # Join the rest of the line as a string
        if (raw_string.startswith('"') and raw_string.endswith('"')) or \
           (raw_string.startswith("'") and raw_string.endswith("'")):        # If the string is enclosed in quotes (single or double)
            string_literal = raw_string[1:-1]                                # Remove the quotes
            program.append(string_literal)                                   # Add the string to the program
            token_counter += 1                                               # Increment the token counter
        else:
            raise ValueError(f"Invalid string literal in PRINT: {line}")     # Gracefully raise a program error

    elif opcode in ["JUMP", "JUMP.IF.0", "JUMP.IF.POS"]:
        # Expects a label
        label = line_parts[1]
        if label not in label_tracker:
            raise ValueError(f"Undefined label '{label}' in {opcode}")
        program.append(label)
        token_counter += 1

    elif opcode == "LOOP":
        # Expects a line number and a repeat count
        try:
            line_number = int(line_parts[1])
            repeat_count = int(line_parts[2])
            program.append(line_number)
            program.append(repeat_count)
            token_counter += 2
        except (IndexError, ValueError):
            raise ValueError(f"Invalid LOOP format: {line}")

    elif opcode == "WAIT":
        # Expects a number
        try:
            number = int(line_parts[1])
            program.append(number)
            token_counter += 1
        except (IndexError, ValueError):
            raise ValueError(f"Invalid number in WAIT: {line}")

###########################
#     Interpretation      #
###########################

class Stack:
    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
        self.sp = -1
        self.size = size

    def push(self, number):
        if self.sp >= self.size - 1:
            raise IndexError("Stack Overflow")  
        self.sp += 1
        self.buf[self.sp] = number

    def pop(self):
        if self.sp < 0:
            raise IndexError("Stack Underflow")
        number = self.buf[self.sp]
        self.sp -= 1
        return number
    
    def top(self):
        if self.sp < 0:
            raise IndexError("Stack is Empty")
        return self.buf[self.sp]

pc = 0
stack = Stack(256)
loop_tracker = {}

while pc < len(program):

    opcode = program[pc]
    pc += 1

    if opcode == "PUSH":
        number = program[pc]
        pc += 1
        stack.push(number)

    elif opcode == "POP":
        stack.pop()

    elif opcode == "ADD":
        a = stack.pop()
        b = stack.pop()
        stack.push(a + b)

    elif opcode == "SUB":
        a = stack.pop()
        b = stack.pop()
        stack.push(b - a)

    elif opcode == "MUL":
        a = stack.pop()
        b = stack.pop()
        stack.push(a * b)

    elif opcode == "DIV":  
        a = stack.pop()
        b = stack.pop()
        if a == 0:
            raise ZeroDivisionError("Division by zero")
        stack.push(b // a)

    elif opcode == "PRINT":
        string_literal = program[pc]
        pc += 1
        print(string_literal)

    elif opcode == "READ":
        try:
            value = int(input())  
            stack.push(value)
        except ValueError:
            print("Error: Invalid input. Must be an integer.", file=sys.stderr)
            exit(1)

    elif opcode == "JUMP":
        label = program[pc]
        pc = label_tracker[label]

    elif opcode == "JUMP.IF.0":
        number = stack.top()
        if number == 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1

    elif opcode == "JUMP.IF.POS":
        number = stack.top()
        if number > 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1

    elif opcode == "LOOP":
        line_number = int(program[pc])  # Jump line
        pc += 1
        repeat_count = int(program[pc])  # Times to repeat
        pc += 1

        loop_key = f"LOOP-{line_number}"

        if loop_key not in loop_tracker:
            loop_tracker[loop_key] = repeat_count  # Initialize repeat count

        if loop_tracker[loop_key] > 0:
            loop_tracker[loop_key] -= 1
            pc = line_number  # Jump to specified line number
        else:
            del loop_tracker[loop_key]

    elif opcode == "HALT":
        break

    elif opcode == "DUP":
        stack.push(stack.top())

    elif opcode == "SWAP":
        a = stack.pop()
        b = stack.pop()
        stack.push(a)
        stack.push(b)

    elif opcode == "OVER":
        a = stack.pop()
        b = stack.pop()
        stack.push(b)
        stack.push(a)
        stack.push(b)

    elif opcode == "ROT":
        a = stack.pop()
        b = stack.pop()
        c = stack.pop()
        stack.push(b)
        stack.push(a)
        stack.push(c)

    elif opcode == "NIP":
        a = stack.pop()
        stack.pop()
        stack.push(a)

    elif opcode == "TUCK":
        a = stack.pop()
        b = stack.pop()
        stack.push(a)
        stack.push(b)
        stack.push(a)

    elif opcode == "PRINT.TOP":
        print(stack.top())

    elif opcode == "WAIT":
        number = program[pc]
        pc += 1
        sleep(number)
