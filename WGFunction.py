
#Rubi Yanto - C00163855 - 28/11/2014

import random
import contains

class WGFunction:
    urlOfDict03 = 'dictionaries/dict03'
    urlOfDict07 = 'dictionaries/dict07'
    countOfDict03 = 19198    # 3 - 6
    countOfDict07 = 53354    # from 7 up

    @staticmethod
    def is_guessword_in_word(guessword, word):
        return contains.contains(word, guessword)
    @staticmethod
    def is_word_in_dict(word, dict):
        with open(dict,"r") as wds:
            for wd in wds:
                if word.strip() == wd.strip():
                    return True
        return False


def get_random_word(_dict, count):
    word = None
    f = open(_dict)
    r = random.randint(1, count)
    for i, ln in enumerate(f):
        if i == r:
            word = f.readline().rstrip()
            break
    f.close()
    return word


