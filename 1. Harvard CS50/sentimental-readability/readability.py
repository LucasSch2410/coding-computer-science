# TODO
from cs50 import get_string


def main():
    text = get_string("Text: ")

    calculates_class(text)


def calculates_class(text):
    letters = 0
    for letter in text:
        if letter.isalpha():
            letters += 1

    words = len(text.split(" "))

    sentences = 0
    for letter in text:
        if (letter == ".") or (letter == "!") or (letter == "?"):
            sentences += 1

    L = 100 * (letters / words)
    S = 100 * (sentences / words)

    index = int(round(0.0588 * L - 0.296 * S - 15.8))

    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print("Grade", index)


main()
