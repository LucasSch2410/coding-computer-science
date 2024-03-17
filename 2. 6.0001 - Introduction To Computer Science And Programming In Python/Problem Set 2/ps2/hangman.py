# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''        
    
    return all(letter in letters_guessed for letter in secret_word)



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    
    return_guessed = ''
    for letter_secret in secret_word:
        if letter_secret in letters_guessed:
            return_guessed += letter_secret
        else:
            return_guessed += '_ '
            
    return return_guessed
        


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    letters_remaining = ''
    for letter in string.ascii_lowercase:
        if letter in letters_guessed:
            continue
        letters_remaining += letter
    
    return letters_remaining
    
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    guesses_remaining = 6
    letters_guessed = ''
    warnings_remaining = 3
    
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    
    while guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed):
        print("-" * 13)
        print(f"You have {guesses_remaining} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}.")
        
        guess = input("Please guess a letter: ")
        
        if not str.isalpha(guess):
            if warnings_remaining > 0:
                print(f"Oops! That is not a valid letter. You have {warnings_remaining} "
                 f"warnings left: {get_guessed_word(secret_word, letters_guessed)}")
                warnings_remaining -= 1

            else:
                guesses_remaining -= 1
                print(f"Oops! That is not a valid letter. You have no warnings left "
                 f"so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}")
            continue
        
        guess = str.lower(guess)
        
        if guess in letters_guessed:
            if warnings_remaining > 0:
                print(f"Oops! You've already guessed that letter. You have {warnings_remaining} "
                 f"warnings left: {get_guessed_word(secret_word, letters_guessed)}")
                warnings_remaining -= 1

            else:
                guesses_remaining -= 1
                print(f"Oops! You've already guessed that letter. You have no warnings left "
                 f"so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}")
            continue
        
        letters_guessed += guess

        if guess in secret_word:
            print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
        else:
            if guess in 'aeiou':    
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
            print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
            
    print("-" * 13)

    if guesses_remaining < 1 and not is_word_guessed(secret_word, letters_guessed):
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")
    else:
        print("Congratulations, you won!")
        print(f"Your total score for this game is: {guesses_remaining * len(letters_guessed)}")

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    word = my_word.replace(" ", "")
    match_dict = dict()
    guessed_word = ''
        
    if len(word) == len(other_word):
        for i in range(len(word)):
            match_dict[i] = (word[i], other_word[i])

        values = list(match_dict.values())
        
        for value in values:
            if value[1] not in guessed_word and value[0] == '_':
                guessed_word += value[1]
            elif value[1] in guessed_word and value[0] != '_':
                return False
            
            if value[0] == '_':
                continue
            
            if value[0] != value[1]:
                return False

        return True
    else:
        return False
            
    

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    
    possible_matches = []
    
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches.append(word)
            
    if len(possible_matches) > 0:    
        print(possible_matches)
    else:
        print('No matches found')

    

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    guesses_remaining = 6
    letters_guessed = ''
    warnings_remaining = 3
    
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    
    while guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed):
        print("-" * 13)
        print(f"You have {guesses_remaining} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}.")
        
        guess = input("Please guess a letter: ")
        
        if guess == "*":
            print("Possible word matches are: ")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue
        
        if not str.isalpha(guess):
            if warnings_remaining > 0:
                print(f"Oops! That is not a valid letter. You have {warnings_remaining} "
                 f"warnings left: {get_guessed_word(secret_word, letters_guessed)}")
                warnings_remaining -= 1

            else:
                guesses_remaining -= 1
                print(f"Oops! That is not a valid letter. You have no warnings left "
                 f"so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}")
            continue
        
        guess = str.lower(guess)
        
        if guess in letters_guessed:
            if warnings_remaining > 0:
                print(f"Oops! You've already guessed that letter. You have {warnings_remaining} "
                 f"warnings left: {get_guessed_word(secret_word, letters_guessed)}")
                warnings_remaining -= 1

            else:
                guesses_remaining -= 1
                print(f"Oops! You've already guessed that letter. You have no warnings left "
                 f"so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}")
            continue
        
        letters_guessed += guess

        if guess in secret_word:
            print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
        else:
            if guess in 'aeiou':    
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
            print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
            
    print("-" * 13)

    if guesses_remaining < 1 and not is_word_guessed(secret_word, letters_guessed):
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")
    else:
        print("Congratulations, you won!")
        print(f"Your total score for this game is: {guesses_remaining * len(letters_guessed)}")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
