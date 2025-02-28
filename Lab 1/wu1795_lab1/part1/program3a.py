index = int(input("How many Fibonacci numbers would you like to generate? "))

fib0 = 0
fib1 = 1

fib_seq = []
for i in range(index):
    fib_seq.append(fib0)
    temp_fib = fib0
    fib0 = fib1
    fib1 = temp_fib + fib1
        
print("The Fibonacci sequence is:", ', '.join(map(str, fib_seq)))