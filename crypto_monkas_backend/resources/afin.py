from flask_restful import Resource, reqparse
from itertools import product
from sys import path

if "../common" not in path:
    path.append("../common")

from common import utils


def afin_key(value: str) -> int:
    value = "".join([c if (c.isdecimal() or c.isspace()) else "" for c in value])
    value = value.split()
    try:
        value_a = int(value[0]) % 26
    except IndexError:
        raise ValueError("No A argument was provided")
    except ValueError:
        raise ValueError("A Argument can't be parse as integer")
    if value_a % 2 == 0 or value_a % 13 == 0:
        raise ValueError("Key is not invertible")
    try:
        value_b = int(value[1]) % 26
    except IndexError:
        raise ValueError("No B argument was provided")
    except ValueError:
        raise ValueError("B Argument can't be parse as integer")

    return (value_a, value_b)


def head_value(value: str) -> int:
    value = value.split(" ")
    try:
        value = int(value[0])
    except ValueError:
        raise ValueError("Argument can't be parse as integer")
    if value <= 0 or 26 < value:
        raise ValueError("Argument out of range of possibilities")
    return value


afin_enc_parser = reqparse.RequestParser()
afin_enc_parser.add_argument(
    "plaintext", type=utils.plaintext, required=True, help="plaintext is required"
)
afin_enc_parser.add_argument(
    "key", type=afin_key, required=True, help="unvalid argument {error_msg}"
)

afin_dec_parser = reqparse.RequestParser()
afin_dec_parser.add_argument(
    "ciphertext", type=utils.ciphertext, required=True, help="ciphertext is required"
)
afin_dec_parser.add_argument(
    "key", type=afin_key, required=True, help="unvalid argument {error_msg}"
)

afin_atk_parser = reqparse.RequestParser()
afin_atk_parser.add_argument(
    "ciphertext", type=utils.ciphertext, required=True, help="ciphertext is required"
)
afin_atk_parser.add_argument(
    "head", type=head_value, required=True, help="unvalid_argument {error_msg}"
)


class AfinEnc(Resource):
    def get(self):
        args = afin_enc_parser.parse_args()
        plaintext = args["plaintext"]
        key = args["key"]
        ciphertext = "".join(
            [utils.chr_up((utils.ascci_code(c) * key[0] + key[1]) % 26) for c in plaintext]
        )
        return {"ciphertext": ciphertext}


class AfinDec(Resource):
    def get(self):
        args = afin_dec_parser.parse_args()
        ciphertext = args["ciphertext"]
        key = args["key"]
        plaintext = "".join(
            [utils.chr_low(((utils.ascci_code(c) - key[1]) * pow(key[0], -1, 26)) % 26) for c in ciphertext]
        )
        return {"plaintext": plaintext}


class AfinAtk(Resource):
    def get(self):
        args = afin_atk_parser.parse_args()
        ciphertext = args["ciphertext"]
        head = args["head"]
        a_keys = filter(lambda x: not(x % 13 == 0 or x % 2 == 0), range(26))
        b_keys = range(26)
        plaintexts_keys = [
            ["".join([utils.chr_low(((utils.ascci_code(c) - key[1]) * pow(key[0], -1, 26)) % 26) for c in ciphertext]), key]
            for key in product(a_keys, b_keys)
        ]
        plaintexts, keys = zip(*sorted(plaintexts_keys, key=lambda x: utils.diff_rank(x[0])))
        return {"plaintexts": plaintexts[0:head], "keys": keys[0:head]}
