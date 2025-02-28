birthdays = {
    "Ada Lovelace": "12/10/1815",
    "Albert Einstein": "3/14/1879",
    "Benjamin Franklin": "1/17/1706",
    "George Washington": "2/22/1732",
    "Neil Armstrong": "8/5/1930"
    }

print("Welcome to the birthday dictionary. We know the birthdays of:")
for name in birthdays:
    print(name)
    
input_name = input("Whose birthday do you want to look up? ")

if input_name in birthdays:
    print(input_name + "'s birthday is " + birthdays[input_name] + ".")
else:
    print("Name not found in dictionary.")