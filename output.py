result = 1
while True:
    operation = input()
    operand = input()
    if operation == "*":
        result = result * float(operand)
    elif operation == "MOD":
        result = int(result) % int(operand)
    else:
        print("Invalid Operation Entered")
    print(result)
    quit = input()
    if quit == "quit":
        break