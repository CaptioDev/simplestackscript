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
        label_tracker[opcode[:-1]] = token_counter  # Store the label and its token number
        continue

    program.append(opcode)                          # Add the opcode to the program
    token_counter += 1                              # Increment the token counter

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

    elif opcode == "GOTO":                                                   # ---- If the opcode is GOTO ----

        label = line_parts[1]                                                # Get the label
        if label not in label_tracker:
            raise ValueError(f"Undefined label '{label}' in {opcode}")       # If the label is not defined, raise an error
        program.append(label)                                                # Add the label to the program
        token_counter += 1                                                   # Increment the token counter

    elif opcode == "LOOP":                                                   # ---- If the opcode is LOOP ----
        try:
            label = line_parts[1]                                            # Get the label
            if label not in label_tracker:
                raise ValueError(f"Undefined label '{label}' in {opcode}")   # If the label is not defined, raise an error
            repeat_count = int(line_parts[2])                                # Get the repeat count
            program.append(label)                                            # Add the label to the program         <-| Increment token counter by 2
            program.append(repeat_count)                                     # Add the repeat count to the program  <-| because we added 2 tokens
            token_counter += 2                                               # Increment the token counter by 2 ------| to the program counter!
        except (IndexError, ValueError):
            raise ValueError(f"Invalid LOOP format: {line}")                 # If the format is invalid, raise an error

    elif opcode == "WAIT":                                                   # ---- If the opcode is WAIT ----
        try:
            number = int(line_parts[1])                                      # Parse the number
            program.append(number)                                           # Add the number to the program
            token_counter += 1                                               # Increment the token counter
        except (IndexError, ValueError):
            raise ValueError(f"Invalid number in WAIT: {line}")              # If the number is not valid, raise an error
    
    # TODO: IF OPCODE, SEE BELOW
    # 
    # The IF opcode has three arguments: IF [<|>|=] <number> <secondary_opcode> ...
    # This allows conditional logic where if the top of the stack is greater than, less than,
    # or equal to, a different opcode can start.

##################################################
#                 Interpretation                 #
##################################################

class Stack:                                                    # Start the stack memory
    def __init__(self, size):
        self.array = [0 for _ in range(size)]                   # Initialize the stack with zeros
        self.sp = -1                                            # Initialize the pointer right before the stack
        self.size = size

    def push(self, number):                                     # Stack push function
        if self.sp >= self.size - 1:                            # If the pointer is pointing beyond stack memory
            raise IndexError("Stack Overflow")                  # Gracefully raise stack overflow error
        self.sp += 1                                            # Move pointer to front of stack
        self.array[self.sp] = number                            # Assign stack value to number

    def pop(self):                                              # Stack pop functionality
        if self.sp < 0:                                         # If the pointer is pointing below stack memory
            raise IndexError("Stack Underflow")                 # Gracefully raise stack underflow error
        number = self.array[self.sp]                            # Get top value of stack
        self.sp -= 1                                            # Move pointer to the next back of the stack
        return number                                           # Return number for optional further processing
    
    def top(self):                                              # Stack top functionality
        if self.sp < 0:                                         # If the pointer is pointing below stack memory
            raise IndexError("Stack is Empty")                  # Gracefully raise stack empty error
        return self.array[self.sp]                              # Return top of stack for processing

pc = 0                                          # Instantiate the program counter
stack = Stack(256)                              # Instantiate the stack memory
loop_tracker = {}                               # Instantiate loop tracking

while pc < len(program):                        # Start the program loop

    opcode = program[pc]                        # Load first opcode for processing
    pc += 1                                     # Increase program counter

    if opcode == "PUSH":                        # Adds a number to the stack memory
        number = program[pc]
        pc += 1
        stack.push(number)

    elif opcode == "POP":                       # Removes a number from stack memory
        stack.pop()

    elif opcode == "ADD":                       # Adds two numbers from stack memory
        a = stack.pop()                         # It removes the top two numbers from stack to add, then pushes
        b = stack.pop()
        stack.push(a + b)

    elif opcode == "SUB":                       # Subtracts two numbers from stack memory
        a = stack.pop()                         # It removes the top two numbers from stack to subtract, then pushes
        b = stack.pop()
        stack.push(b - a)

    elif opcode == "MUL":                       # Multiplies two numbers from stack memory
        a = stack.pop()                         # Same thing as add and subtract...
        b = stack.pop()
        stack.push(a * b)

    elif opcode == "DIV":                       # Same thing as add, subtract, and multipy...
        a = stack.pop()                         # With graceful divide by zero error
        b = stack.pop()
        if a == 0:
            raise ZeroDivisionError("Division by zero")
        stack.push(b // a)

    elif opcode == "PRINT":                     # Logic to print to screen
        string_literal = program[pc]
        pc += 1
        print(string_literal)

    elif opcode == "READ":                      # Logic to read user input
        try:
            value = int(input())  
            stack.push(value)
        except ValueError:
            raise ValueError("Invalid integer input")

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
