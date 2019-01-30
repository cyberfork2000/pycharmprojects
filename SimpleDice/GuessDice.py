from random import randint

for i in range(0, 3):
    x = randint(1, 6)

    guess = input("Guess dice value? ")
    if guess == x:
        print ("you're correct with attempt i+1")
        break
    else:
        print ("incorrect, try again")


