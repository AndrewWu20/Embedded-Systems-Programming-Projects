a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
print("a =", a)

number = int(input("Enter a number: "))

filtered_list = []
for num in a:
    if num < number:
        filtered_list.append(num)
        
print("The new list is", filtered_list)