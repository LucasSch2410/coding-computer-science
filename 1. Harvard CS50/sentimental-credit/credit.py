# TODO
from cs50 import get_string


def main():
    # Prompt for input
    card = get_string("Number: ")

    # Calculate checksum
    checksum, length = calculate_card_checksum(card)

    # Check for card length and starting digits
    verifyCard(checksum, card, length)


def calculate_card_checksum(card_number):
    total_sum = 0
    length = 0
    current_digit = 0

    while current_digit != card_number:
        length += 1
        # Catch the last digit in the card
        current_digit = card_number[-length:]

        even_number = 0
        odd_sum = 0

        # Verify if the number is odd or even
        if length % 2:
            odd_sum = int(current_digit[0])
        else:
            first_sum = int(current_digit[0]) * 2
            # If the number is greater than 9, sum the digits
            if first_sum >= 10:
                digits = [int(digit) for digit in str(first_sum)]
                even_number += digits[0] + digits[1]
            else:
                even_number += first_sum

        total_sum += even_number + odd_sum

    return total_sum, length


def verifyCard(checksum, card, length):
    if 12 < length < 17 and checksum % 10 == 0:
        firstNumbers = int(card[:2])
        if (firstNumbers == 34 or firstNumbers == 37) and length == 15:
            print("AMEX")
        elif 50 < firstNumbers < 56 and length == 16:
            print("MASTERCARD")
        elif 40 <= firstNumbers < 50 and (length == 13 or length == 16):
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")


main()
