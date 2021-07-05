# array of what each number should look like in an account_numbers file, from 0-9
NUMBER_DEFS = (
    (
        ' _ ',
        '| |',
        '|_|'
    ),
    (
        '   ',
        '  |',
        '  |'
    ),
    (
        ' _ ',
        ' _|',
        '|_ '
    ),
    (
        ' _ ',
        ' _|',
        ' _|'
    ),
    (
        '   ',
        '|_|',
        '  |'
    ),
    (
        ' _ ',
        '|_ ',
        ' _|'
    ),
    (
        ' _ ',
        '|_ ',
        '|_|'
    ),
    (
        ' _ ',
        '  |',
        '  |'
    ),
    (
        ' _ ',
        '|_|',
        '|_|'
    ),
    (
        ' _ ',
        '|_|',
        ' _|'
    )
)

def generate_garbled_numbers():
    # create array to store garbled variations of each number
    # this array takes the structure of the following:
    # 1st layer, each element represents a number from 0-9
    # 2nd layer represents each variation with one character garbled
    # 3rd layer is an array of each line of the letter structure
    results = []
    # iterate from 0 to 9, inclusive
    for i in range(10):
        # take the original number from the NUMBER_DEFS global variable
        number_def = NUMBER_DEFS[i]
        # start a new blank 2nd-level array for this number
        results.append([])
        # join the 3 lines of the string together for easier processing
        number_string = "".join(number_def)
        # enumerate over the string representation of the number
        for j, c in enumerate(number_string):
            # if the character is a space
            if c == " ":
                # make copies of it as lists so that
                # a. you're not editing the original and
                # b. it's mutable to allow replacing a character at an index
                number_copy1 = list(number_string)
                number_copy2 = list(number_string)
                # change the character in each copy to a pipe and an underscore
                number_copy1[j] = "|"
                number_copy2[j] = "_"
                # rejoin the lists to strings
                number_copy1 = "".join(number_copy1)
                number_copy2 = "".join(number_copy2)
                # construct the new variation and append it to this number's 2nd-level array
                # do so using a tuple because this won't be modified in the future
                # and using tuples is more memory-efficient
                results[i].append(
                    (
                        number_copy1[0:3],
                        number_copy1[3:6],
                        number_copy1[6:9]
                    )
                )
                results[i].append(
                    (
                        number_copy2[0:3],
                        number_copy2[3:6],
                        number_copy2[6:9]
                    )
                )
            else:
                # as above, except replacing either an underscore
                # or a pipe with a space
                number_copy = list(number_string)
                number_copy[j] = " "
                number_copy = "".join(number_copy)
                results[i].append(
                    (
                        number_copy[0:3],
                        number_copy[3:6],
                        number_copy[6:9]
                    )
                )
    # return the variations/garbled numbers
    return results

# generate the garbled numbers and store 
# them in a global variable
GARBLED_NUMBERS = generate_garbled_numbers()

def is_valid_acc_no(acc_no):
    """
    Checks if an account number is valid using the checksum:
    (1*d1+2*d2+3*d3+...+9*d9) mod 11 = 0
    where
    account number - x  x  x  x  x  x  x  x  x
    position names - d9 d8 d7 d6 d5 d4 d3 d2 d1

    Parameters
    ----------
    acc_no : str
        the account number to validate.
    
    Outputs
    -------
    result : boolean
    """
    # if there's a "?" in the acc_no or it's not 9 digits long then we can't even try to validate it
    if "?" in acc_no or len(acc_no) != 9:
        raise Exception(f"account number {acc_no} has an incorrect amount of digits and cannot be validated")
    else:
        # split acc_no into a list of ints so that we can do math with them
        acc_no = [int(i) for i in acc_no]
        # create list of inverted weights for the checksum calculation
        mults = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        # create a total started at zero for the calculation
        total = 0
        # iterate over both acc_no and mults together
        for i, j in zip(acc_no, mults):
            # add their product to total
            total += i*j
        # if total modulo 11 is zero then the checksum passes
        if total % 11 == 0:
            return True
        # otherwise it fails
        else:
            return False

def parse_acc_no(account_number):
    """
    Parse an account number that's spread out over three lines. 
    E.g. 
        _  _  _  _  _  _     _ 
    |_||_|| || ||_   |  |  ||_ 
      | _||_||_||_|  |  |  | _|

    Return account number as a string of digits
    --> 490067715

    Parameters
    ----------
    account_number: list
        list of three strings, 
        with each string 27 characters long

    Outputs
    -------
    result : str
    """
    # create a list to contain each of the separate digits sequentially
    # extracted from account_number
    digits = []
    # create list for digits parsed and processed as numbers/unknown("?")
    result = []
    # iterate 9 times, once for each number
    for i in range(9):
        # construct and append the individual digit to "digits" list
        digits.append(
            (
                # use iterator and multiples of three to get each letter
                account_number[0][(i*3):(i*3+3)],
                account_number[1][(i*3):(i*3+3)],
                account_number[2][(i*3):(i*3+3)],
            )
        )
    # iterate over each digit
    for digit in digits:
        # if the digit matches one of the defined 0-9 digits
        if digit in NUMBER_DEFS:
            # add it to results
            result.append(str(NUMBER_DEFS.index(digit)))
        else:
            # otherwise add a "?"
            result.append("?")
    # check that the result is 9 digits
    if len(result) == 9:
        # return a string of the result
        return "".join(result)
    else:
        raise Exception(f"Did not find 9 numbers in account number")

def count_different_characters(string1, string2):
    """
    Takes two equal-length strings and counts how many characters in sequence are different

    Parameters
    ----------
    string1 : str
    string2 : str

    Outputs
    -------
    counter : int
    """
    # create a counter
    counter = 0
    # if the two strings are of different lengths, abandon ship
    if len(string1) != len(string2):
        raise Exception(f"Can't compare two strings of a different length.")
    
    # iterate over both at the same time
    for a, b in zip(string1, string2):
        # and if they're not equal, increment the counter
        if a != b:
            counter += 1
    return counter

def get_valid_acc_nos_with_guessed_numbers(account_number):
    """
    Given an account_number (the 3-line, 27-character format)
    which doesn't match the pre-baked 0-9,
    try to generate guesses that are valid by changing one character from
    a space to an underscore or pipe, and vice versa.

    This method is exhaustive and greedy, it will first generate all
    permutations, then it will exclude those which have changed 
    more than 1 character

    Parameters
    ----------
    account_number : list
        list of three strings, 
        with each string 27 characters long

    Outputs
    -------
    valid_guesses : list of str
    """
    # run the normal parse_acc_no to see where the "?"s are
    acc_no = parse_acc_no(account_number)
    # construct a list to hold exhaustive guesses in
    guesses = []
    # construct a 2D list to hold the possible permutations of each digit 
    result_with_alts = [[i,] if i!="?" else [] for i in acc_no]
    # for each character in the parsed acc_no
    for i, character in enumerate(acc_no):
        # get the raw character from account_number for this 
        # corresponding digit of acc_no
        raw_character = (
            account_number[0][(i*3):(i*3+3)],
            account_number[1][(i*3):(i*3+3)],
            account_number[2][(i*3):(i*3+3)],
        )
        # enumerate each layer of the 3D array of garbled numbers
        for j, number_alts in enumerate(GARBLED_NUMBERS):
            for alt in number_alts:
                # if the character matches the garbled one
                if raw_character == alt:
                    # add the index of the number (which is the digit itself) 
                    # to this character in result_with_alts
                    result_with_alts[i].append(str(j))

    # now we exhaustively generate every permutation of the account number
    # substituting each character with a matching alt that we found
    for i0 in result_with_alts[0]:
        for i1 in result_with_alts[1]:
            for i2 in result_with_alts[2]:
                for i3 in result_with_alts[3]:
                    for i4 in result_with_alts[4]:
                        for i5 in result_with_alts[5]:
                            for i6 in result_with_alts[6]:
                                for i7 in result_with_alts[7]:
                                    for i8 in result_with_alts[8]:
                                        # if it's only changed one character
                                        if count_different_characters(
                                            f"{i0}{i1}{i2}{i3}{i4}{i5}{i6}{i7}{i8}", 
                                            acc_no
                                        ) == 1:
                                            # add it to guesses
                                            guesses.append(f"{i0}{i1}{i2}{i3}{i4}{i5}{i6}{i7}{i8}")

    # create an array for valid guesses
    valid_guesses = []
    # iterate over all guesses
    for guess in guesses:
        # and try to validate them
        if is_valid_acc_no(guess):
            # if they're valid, add them to valid_guesses
            valid_guesses.append(guess)
    # not necessary to force unique values, but better safe than sorry
    return list(set(valid_guesses))

def generate_fixed_file(account_numbers):
    """
    Given a list of account numbers (the 3-lines of 27-characters format),
    output a file containing each account number parsed, with indicators for those
    believed to be erroneous, invalid, or ambiguous

    Args:
    account_number: list of three strings, 
    with each string 27 characters long
    """
    # open a file to write the results to
    with open("outputs.txt", "w") as f:
        # iterate over each account_number
        for account_number in account_numbers:
            # attempt to parse it
            acc_no = parse_acc_no(account_number)
            # if it contains only one unknown character then
            # we want to guess the missing one
            if acc_no.count("?") == 1:
                # generate list of valid guesses
                valid_guesses = get_valid_acc_nos_with_guessed_numbers(account_number)
                # if we only got one valid guess, then that's the correct account number
                # and we should write it to the file
                if len(valid_guesses) == 1:
                    f.write(f"{valid_guesses[0]}\n")
                # but if there are no valid guesses then we write the 
                # parsed one and call it ILL
                elif len(valid_guesses) == 0:
                    f.write(f"{acc_no} ILL\n")
                # if there are more than 1 valid guesses then
                # we call it AMB and list the guesses after the parsed one
                else:
                    f.write(f"{acc_no} AMB {valid_guesses}\n")
            # if there are more than 1 "?" then we won't guess, call it ILL
            elif acc_no.count("?") > 1:
                f.write(f"{acc_no} ILL\n")
            # if there are no "?"s in the parsed account number
            else:
                # if it's valid, then write that to the file
                if is_valid_acc_no(acc_no):
                    f.write(f"{acc_no}\n")
                # otherwise, try to guess valid ones by changing one number to
                # a number that's within an error's reach of it
                else:
                    valid_guesses = get_valid_acc_nos_with_guessed_numbers(account_number)
                    # as above, if 1 match, that's the right one
                    # if no matches, it's ERR
                    # if more than 1, it's AMB and list the possible values
                    if len(valid_guesses) == 1:
                        f.write(f"{valid_guesses[0]}\n")
                    elif len(valid_guesses) == 0:
                        f.write(f"{acc_no} ERR\n")
                    else:
                        f.write(f"{acc_no} AMB {valid_guesses}\n")

def parse_input_file(filename):
    """
    parse the input file of account numbers and return them as an array of strings
    """
    with open(filename, "r") as f:
        file_lines = f.read().split("\n")
    account_numbers = []
    for i in range(0, len(file_lines), 4):
        account_numbers.append(
            file_lines[i:i+3]
        )
    return account_numbers

if __name__ == "__main__":
    account_numbers = parse_input_file("account_numbers.txt")
    generate_fixed_file(account_numbers)