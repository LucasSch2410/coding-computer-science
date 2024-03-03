# TODO
from cs50 import get_int


def main():
    while True:
        height = get_int("Height: ")
        if height > 0 and height < 9:
            break

    for i in range(height):
        spaces = " " * (height - 1 - i)
        hashes_left = "#" * (i + 1)
        hashes_right = "#" * (i + 1)
        print(f"{spaces}{hashes_left}  {hashes_right}")


main()
