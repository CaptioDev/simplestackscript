import sys

# read filepath
program_filepath = sys.argv[1]

###########################
#      Tokenization       #
###########################

# read file line-by-line
program_lines = []
with open(program_filepath, 'r') as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]

program = []
token_counter = 0
label_tracker = {}
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]

    # check for empty line
    if opcode == "":
        continue

    # check if opcode is a label
    if opcode.endswith(":"):
        label_tracker[opcode[:-1]] = token_counter
        continue

    # store opcode token
    program.append(opcode)
    token_counter += 1

    # handle opcodes
    if opcode == "PUSH":
        # expects a number
        number = int(parts[1])
        program.append(number)
        token_counter += 1
    elif opcode == "PRINT":
        # expects a string literal
        string_literal = ' '.join(parts[1:])[1:-1]
        program.append(string_literal)
        token_counter += 1
    elif opcode == "JUMP.IF.0":
        # expects a label
        label = parts[1]
        program.append(label)
        token_counter += 1
    elif opcode == "JUMP.IF.POS":
        # expects a label
        label = parts[1]
        program.append(label)
        token_counter += 1
    elif opcode == "LOOP":
        line_number = int(parts[1])
        # store the target line number
        program.append(line_number)
        token_counter += 1

###########################
#     Interpretation      #
###########################

class Stack:

    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
        self.sp = -1
        self.size = size

    def push(self, number):
        # check for overflow
        if self.sp >= self.size - 1:
            # overflow error
            raise IndexError("Stack Overflow")  
        self.sp += 1
        self.buf[self.sp] = number

    def pop(self):
        number = self.buf[self.sp]
        self.sp -= 1
        return number
    
    def top(self):
        return self.buf[self.sp]
    

pc = 0
stack = Stack(512)

while program[pc] != "HALT":
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

        result = a - b
        stack.push(-result)
    elif opcode == "MUL":
        a = stack.pop()
        b = stack.pop()

        stack.push(a * b)
    elif opcode == "DIV":  
        a = stack.pop()
        b = stack.pop()

        stack.push(a // b)
    elif opcode == "PRINT":
        string_literal = program[pc]
        pc += 1

        print(string_literal)
    elif opcode == "READ":
        try:
            value = int(input())  # Read input INSIDE the READ instruction
            stack.push(value)
        except ValueError:
            print("Error: Invalid input. Must be an integer.", file=sys.stderr)
            exit(1)
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
        line_number = program[pc]
        # check if line_number is valid
        if line_number < 0 or line_number >= len(program):
            raise IndexError("Invalid line number for LOOP")

        pc = line_number
        continue
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