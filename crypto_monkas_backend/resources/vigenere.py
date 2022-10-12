from flask_restful import Resource, reqparse
from collections import Counter
from itertools import product
import numpy as np
from sys import path

if "../common" not in path:
    path.append("../common")

from common import utils


def vig_key(value: str) -> int:
    value = "".join([c if (c.isalpha() or c.isspace()) else "" for c in value]).upper()
    value = value.split()
    try:
        value = value[0]
    except IndexError:
        raise ValueError("No valid argument was provided")

    return value


vig_enc_parser = reqparse.RequestParser()
vig_enc_parser.add_argument(
    "plaintext", type=utils.plaintext, required=True, help="plaintext is required"
)
vig_enc_parser.add_argument(
    "key", type=vig_key, required=True, help="unvalid argument: {error_msg}"
)

vig_dec_parser = reqparse.RequestParser()
vig_dec_parser.add_argument(
    "ciphertext", type=utils.ciphertext, required=True, help="ciphertext is required"
)
vig_dec_parser.add_argument(
    "key", type=vig_key, required=True, help="unvalid argument: {error_msg}"
)

vig_atk_parser = reqparse.RequestParser()
vig_atk_parser.add_argument(
    "ciphertext", type=utils.ciphertext, required=True, help="ciphertext is required"
)


class VigEnc(Resource):
    def get(self):
        args = vig_enc_parser.parse_args()
        plaintext = args["plaintext"]
        key = args["key"]
        ciphertext = "".join(
            [
                utils.chr_up(
                    (utils.ascci_code(c) + utils.ascci_code(key[i % len(key)])) % 26
                )
                for i, c in enumerate(plaintext)
            ]
        )
        return {"ciphertext": ciphertext}


class VigDec(Resource):
    def get(self):
        args = vig_dec_parser.parse_args()
        ciphertext = args["ciphertext"]
        key = args["key"]
        plaintext = "".join(
            [
                utils.chr_low(
                    (utils.ascci_code(c) - utils.ascci_code(key[i % len(key)])) % 26
                )
                for i, c in enumerate(ciphertext)
            ]
        )
        return {"plaintext": plaintext}


class VigAtk(Resource):
    def get(self):
        args = vig_atk_parser.parse_args()
        ciphertext = args["ciphertext"]
        cipher_sections = list(
            map(
                "".join,
                zip(ciphertext, ciphertext[::1], ciphertext[::2], ciphertext[::3]),
            )
        )
        counts = Counter(cipher_sections)
        repeated = [c for c, count in counts.items() if count > 1]
        distances = []
        for c in repeated:
            indexes = [i for i, value in enumerate(cipher_sections) if value == c]
            distance_candidates = [b - a for a, b in zip(indexes, indexes[1:])]
            mcd = np.gcd.reduce(distance_candidates)
            if mcd > 1:
                distances.append(mcd)
        key_lenght = max(distances, key=distances.count)

        ##return {"plaintexts": plaintexts, "keys": final_keys}
