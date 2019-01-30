numerals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_value(roman_number):
    total = 0
    i = 0
    while i < len(roman_number):
        digit = numerals[roman_number[i]]
        if i == len(roman_number)-1:
            next_digit = 0
        else:
            next_digit = numerals[roman_number[i + 1]]
        if next_digit > digit:
            # take next digit and minus from current digit
            new_value = int(next_digit) - int(digit)
            total += new_value
            i += 2
        else:
            total += int(digit)
            i += 1
    print("Final value is " + str(total))


roman_value("MCMLXXIV")
roman_value("MCMLXXVIII")
roman_value("MLXVI")
roman_value("MMI")
roman_value("I")
roman_value("VI")
roman_value("IV")
roman_value("I")
roman_value("XI")
roman_value("IX")

