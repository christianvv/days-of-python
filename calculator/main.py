import art

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}

#print(operations["*"](4, 8))

def calculator():
    print(art.logo)
    continue_last = True

    num1 = float(input("What is the first number?: "))
    while continue_last:
        for operator in operations:
            print(operator)

        symbol = input("Pick an operation: ")
        num2 =float(input("What's the next number?: "))
        answer = operations[symbol](num1, num2)
        print(f"{num1} {symbol} {num2} = {answer}")

        choice = input(f"Type 'y' to continue calculating with {answer}, or type 'n' to start a new calculation: ").lower()

        if choice == "y":
            num1 = answer
        else:
            continue_last = False
            print("\n * 50")
            calculator()

calculator()
