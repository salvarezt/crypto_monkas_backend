from string import ascii_lowercase, ascii_uppercase
from collections import Counter

MONOFREQ = {
    "e": 12.70,
    "t": 9.06,
    "a": 8.17,
    "o": 7.51,
    "i": 6.97,
    "n": 6.75,
    "s": 6.33,
    "h": 6.09,
    "r": 5.99,
    "d": 4.25,
    "l": 4.03,
    "c": 2.78,
    "u": 2.76,
    "m": 2.41,
    "w": 2.36,
    "f": 2.23,
    "g": 2.02,
    "y": 1.97,
    "p": 1.93,
    "b": 1.29,
    "v": 0.98,
    "k": 0.77,
    "j": 0.15,
    "x": 0.15,
    "q": 0.10,
    "z": 0.07,
}

BIFREQ = {
    "th": 3.56,
    "of": 1.17,
    "io": 0.83,
    "he": 3.07,
    "ed": 1.17,
    "le": 0.83,
    "in": 2.43,
    "is": 1.13,
    "ve": 0.83,
    "er": 2.05,
    "it": 1.12,
    "co": 0.79,
    "an": 1.99,
    "al": 1.09,
    "me": 0.79,
    "re": 1.85,
    "ar": 1.07,
    "de": 0.76,
    "on": 1.76,
    "st": 1.05,
    "hi": 0.76,
    "at": 1.49,
    "to": 1.05,
    "ri": 0.73,
    "en": 1.45,
    "nt": 1.04,
    "ro": 0.73,
    "nd": 1.35,
    "ng": 0.95,
    "ic": 0.70,
    "ti": 1.34,
    "se": 0.93,
    "ne": 0.69,
    "es": 1.34,
    "ha": 0.93,
    "ea": 0.69,
    "or": 1.28,
    "as": 0.87,
    "ra": 0.69,
    "te": 1.20,
    "ou": 0.87,
    "ce": 0.65,
}


def mono_diff_rank(word: str) -> float:
    word_len = len(word)
    word = Counter(word)
    em = 0
    for key, value in MONOFREQ.items():
        word_value = word.get(key, 0) / word_len
        em += abs((value - word_value))
    em /= len(MONOFREQ)
    return em


def bi_diff_rank(word: str) -> float:
    word_len = len(word)
    word = Counter(
        map(''.join, zip(word, word[1:]))
    )
    em = 0
    for key, value in BIFREQ.items():
        word_value = word.get(key, 0) / (word_len - 1)
        em += abs(value - word_value)
    em /= len(BIFREQ)
    return em


def diff_rank(word: str) -> float:
    return mono_diff_rank(word) + bi_diff_rank(word)


def plaintext(value: str) -> str:
    value = value.lower()
    value = "".join([c if c.isalpha() else "" for c in value])
    return value


def ciphertext(value: str) -> str:
    value = value.upper()
    value = "".join([c if c.isalpha() else "" for c in value])
    return value


def ascci_code(c: str):
    if len(c) > 1:
        raise ValueError("must be single character")
    c = c.lower()
    index = ascii_lowercase.index(c)
    return index


def chr_low(x: int):
    x = x % 26
    return ascii_lowercase[x]


def chr_up(x: int):
    x = x % 26
    return ascii_uppercase[x]
