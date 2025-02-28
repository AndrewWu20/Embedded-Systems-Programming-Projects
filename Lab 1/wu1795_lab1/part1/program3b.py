import random

rand_int = random.randint(0, 10)
win = 0
guesses = 0
while guesses < 3:
    guess = int(input("Enter your guess: "))
    if guess == rand_int:
        win = 1
        break
    guesses += 1
    
if win == 1:
    print("You win!")
else:
    print("You lose!")