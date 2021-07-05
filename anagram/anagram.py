
def word_in_parent(parent_word, child_word):
    '''
    Check if the parent_word contains all of the 
    letters in child_word.

    Parameters
    ----------
    parent_word : str
        the base word to build anagrams from
    child_word : str
        the word we're trying to build using parent_word

    Outputs
    -------
    result : bool
        value of whether or not
        child_word can be made from parent_word
    parent_word: str
        String value of parent word. 
        If result == True then return 
        parent_word without the letters 
        of child_word
    '''
    # create a copy of the parent word so that
    # we can modify the copy without affecting
    # the original
    temp_parent_word = parent_word+""
    # iterate over child_word
    for letter in child_word:
        # if the letter exists in temp_parent_word
        if letter in temp_parent_word:
            # remove the letter from temp_parent_word
            temp_parent_word = temp_parent_word.replace(letter, "", 1)
        else:
            # print(f"letter {letter} not in {temp_parent_word}, exiting")
            # otherwise, return False and the whole parent_word
            return False, parent_word
    # implicitly passed the test at this point
    # so return True, and parent_word without the letters
    # of child_word
    return True, temp_parent_word

def anagram_kata(source_word, word_list):
    """
    Perform the main challenge of creating a list of two-word
    anagrams from the word provided

    Parameters
    ----------
    source_word : str
        the word we're creating anagrams from
    word_list : list of str
        list of words we will attempt to create
        using source_word
    
    Outputs
    -------
    word_pairs : list of 2-element tuples of str
        E.g. [("asdf", "qwer"), ...]
    """
    # create array for results
    word_pairs = []
    # for each word in word_list
    for word1 in word_list:
        # see if we can make the word out of source_word
        result1, temp_source_word = word_in_parent(source_word, word1)
        # if there was a match
        if result1:
            # then do it again for the remaining letters in temp_source_word
            for word2 in word_list:
                # making a few assumptions here:
                # 1. The same word is allowed to be found twice
                # 2. We don't have to use all the letters in source_word
                result2, temp_source_word = word_in_parent(temp_source_word, word2)
                # if result2 and result1 and len(temp_source_word) == 0:
                # if there was a second match
                if result2:
                    # add it to the results as a tuple
                    word_pairs.append((word1, word2))
    # sort the tuples in word_pairs and then make it unique/distinct
    # i.e. ("asdf", "qwer") is the same anagram pair as ("qwer", "asdf")
    word_pairs = list( # convert set to list
        set( # create unique set
            [
                tuple(sorted(i)) # create sorted copy of tuple
                for i 
                in word_pairs
            ]
        )
    )
    # return list of results
    return word_pairs

if __name__ == "__main__":
    words = []
    source_word = "documenting"
    with open("wordlist.txt", "r") as f:
        wordlist_txt = f.readlines()[1:]
    for l in wordlist_txt:
        line = l[2:]
        for i in range(6):
            words.append(line[i*9:(i*9)+9].strip())
    while "" in words:
        words.remove("")
    
    word_pairs = anagram_kata(source_word, words)
    print(word_pairs)
