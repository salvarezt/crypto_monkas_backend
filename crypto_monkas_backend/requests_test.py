from requests import get

ex1 = """I found myself within a forest dark, for the straightfoward pathway had been lost.
         Ah me! How hard a thing is to say, what was this forest savage, rough, and stern,
         which in the very thought renews the fear. So bitter is it, death is little more..."""

an1 = """DAJPIYHTNZGARDOCDIVAJMZNOYVMFAJMOCZNOMVDBCOAJRVMYKVOCRVTCVYWZZIGJNOVCHZCJRCVMYVOCD
         IBDNOJNVTRCVORVNOCDNAJMZNONVQVBZMJPBCVIYNOZMIRCDXCDIOCZQZMTOCJPBCOMZIZRNOCZAZVMNJW
         DOOZMDNDOYZVOCDNGDOOGZHJMZ"""

an2 = """JQMVTASWOFJCURZUVIJQBOWRTIBKJQBRZOWRBIUEZRJQCIBTLIRZCISZITDOOVFQWRIZAOZQCZIBTIRZUV
         EUWRQWISCZIRCIWRZUWJQBOWRWIHIEOBQMEZIVTWROBVCZUYZUVRZOHOBSRZQMEZRBOVOCWRZOJOIBWQDU
         RROBUWURTOIRZUWFURRFOAQBO"""
an3 = """JIPVQGNZTFOIXJWKJQCIPUFTWGCULIPUWKFTWUCJHKWIPXCUGSCWKXCZKCGEFFQOPTWCKNFKPXKCUGCWKJQHJTWPTCZXKCWXCTWKJTIPUFTWTCYCHFUPVHKCQGTWFUQXKJDKJQWKFYFUZWKPVHKWUFQFXTWKFIFCUTPEJWWFUJTJWGFCWKJTOJWWOFNPUF"""

ROOT = "http://localhost:5000/"


def shift_test():
    print("shift tests")
    tests_enc = [
        ("abcdefg", "a"),
        ("12345", "12"),
        ("abcdef", "54"),
        (ex1, "177"),
    ]
    tests_dec = [
        ("CDEFGH", "a"),
        ("12345", "12"),
        ("CDEFGH", "54"),
        (an1, "177"),
    ]
    tests_atk = [
        (an1, "a"),
        (an1, "35"),
        (an1, "3"),
    ]
    print("encryptions_tests")
    for test in tests_enc:
        print(get(ROOT + "shift/enc", json={"plaintext": test[0], "key": test[1]}).json())
    print("decryption_tests")
    for test in tests_dec:
        print(get(ROOT + "shift/dec", json={"ciphertext": test[0], "key": test[1]}).json())
    print("attack_tests")
    for test in tests_atk:
        print(get(ROOT + "shift/atk", json={"ciphertext": test[0], "head": test[1]}).json())


def afin_test():
    print("afin tests")
    tests_enc = [
        ("abcdefg", "a"),
        ("abcdefg", "15"),
        ("abcdefg", "15 a"),
        ("abcdefg", "13 15"),
        ("12345", "15 5"),
        ("abcdef", "55 25"),
        (ex1, "177 34"),
    ]
    tests_dec = [
        ("ZCFILO", "a"),
        ("ZCFILO", "15"),
        ("ZCFILO", "15 a"),
        ("ZCFILO", "13 15"),
        ("12345", "15 5"),
        ("ZCFILO", "55 25"),
        (an2, "177 34"),
    ]
    tests_atk = [
        (an2, "a"),
        (an2, "35"),
        (an2, "3"),
    ]
    print("encryptions_tests")
    for test in tests_enc:
        print(get(ROOT + "afin/enc", json={"plaintext": test[0], "key": test[1]}).json())
    print("decryption_tests")
    for test in tests_dec:
        print(get(ROOT + "afin/dec", json={"ciphertext": test[0], "key": test[1]}).json())
    print("attack_tests")
    for test in tests_atk:
        print(get(ROOT + "afin/atk", json={"ciphertext": test[0], "head": test[1]}).json())


def subs_test():
    print("subs tests")
    tests_enc = [
        ("abcdefg", "12345678901234567890123456"),
        ("abcdefg", "bcdefg"),
        ("12345", "bcdefghijklmnopqrstuvwxyza"),
        ("abcdef", "cedgfihkjmlonqpsrutwvyxazb"),
        (ex1, "cedgfihkjmlonqpsrutwvyxazb"),
    ]
    tests_dec = [
        ("CEDGFI", "12345678901234567890123456"),
        ("CEDGFI", "bcdefg"),
        ("12345", "bcdefghijklmnopqrstuvwxyza"),
        ("CEDGFI", "cedgfihkjmlonqpsrutwvyxazb"),
        (an3, "cedgfihkjmlonqpsrutwvyxazb"),
    ]
    tests_atk = []
    print("encryptions_tests")
    for test in tests_enc:
        print(get(ROOT + "subs/enc", json={"plaintext": test[0], "key": test[1]}).json())
    print("decryption_tests")
    for test in tests_dec:
        print(get(ROOT + "subs/dec", json={"ciphertext": test[0], "key": test[1]}).json())
    print("attack_tests")
    for test in tests_atk:
        print(get(ROOT + "subs/atk", json={"ciphertext": test[0], "head": test[1]}).json())


if __name__ == "__main__":
    shift_test()
    afin_test()
    subs_test()
