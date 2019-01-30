import random
import string
from pip._vendor.distlib.compat import raw_input

words = ["apple", "pear", "banana", "egg"]
word = random.choice(words)
blanks = "-"
new_word = blanks * len(word)
word_letters = list(new_word)
incorrect_guess = []


def enter_guess():
    guess_letter = raw_input("Enter guess? ")
    return guess_letter


def check_letter_in_word(guess, countdown):
    if guess in word:
        print(guess + " is a good guess, keep a life.  Attempts left: " + str(countdown))
        for i in range(len(new_word)):
            if word[i] == guess:
                word_letters[i] = guess
    else:
        countdown -= 1
        print(guess + " is a bad guess, lose a life.  Attempts left: " + str(countdown))
        incorrect_guess.append(guess)

    print(str(word_letters))
    print("Attempts not in word " + str(incorrect_guess))
    return countdown


def play_hangman():
    print("Word to guess contains " + str(len(word)) + " letters")
    countdown = 9
    while countdown > 0:
        # guess_letter = enter_guess()
        guess_letter = random.choice(string.ascii_letters.lower())
        countdown = check_letter_in_word(guess_letter, countdown) # check letter exists in word
        if blanks in word_letters and countdown > 0:
            print("Try again")
        elif blanks in word_letters and countdown == 0:
            print("Sorry")
            print("answer is " + word)
        else:
            print("winner")
            break


if __name__ == '__main__':
    while play_hangman():
        print()



