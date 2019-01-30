import unittest


class RomanNumerals:

    def roman_value(self, roman_number):
        numerals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        total = 0
        i = 0
        while i < len(roman_number):
            digit = numerals[roman_number[i]]
            if i == len(roman_number) - 1:
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
        return int(total)


print(RomanNumerals().roman_value('MMMCMLXXXVI'))
print(RomanNumerals().roman_value('MMMM'))
print(RomanNumerals().roman_value('C'))