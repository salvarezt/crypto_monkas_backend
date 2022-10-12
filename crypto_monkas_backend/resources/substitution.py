from flask_restful import Resource, reqparse
from collections import Counter
from sys import path

path.append("../common")

from common import utils


def subs_key(value: str) -> int:
    value = value.upper()
    value = [c for c in value if c.isalpha()]
    if len(value) != 26:
        raise ValueError("Argument have a wrong lenght")
    if len(value) != len(set(value)):
        raise ValueError("Argument includes repeat letters")
    return value


subs_enc_parser = reqparse.RequestParser()
subs_enc_parser.add_argument(
    "plaintext", type=utils.plaintext, required=True, help="plaintext is required"
)
subs_enc_parser.add_argument(
    "key", type=subs_key, required=True, help="unvalid argument: {error_msg}"
)

subs_dec_parser = reqparse.RequestParser()
subs_dec_parser.add_argument(
    "ciphertext", type=utils.ciphertext, required=True, help="ciphertext is required"
)
subs_dec_parser.add_argument(
    "key", type=subs_key, required=True, help="unvalid argument: {error_msg}"
)

subs_atk_parser = reqparse.RequestParser()
subs_atk_parser.add_argument(
    "ciphertext", type=utils.ciphertext, required=True, help="ciphertext is required"
)


class SubsEnc(Resource):
    def get(self):
        args = subs_enc_parser.parse_args()
        plaintext = args["plaintext"]
        key = args["key"]
        enc_map = {x: y for x, y in zip(utils.ascii_lowercase, key)}
        ciphertext = "".join(enc_map[x] for x in plaintext)
        return {"ciphertext": ciphertext}


class SubsDec(Resource):
    def get(self):
        args = subs_dec_parser.parse_args()
        ciphertext = args["ciphertext"]
        key = args["key"]
        dec_map = {x: y for x, y in zip(key, utils.ascii_lowercase)}
        plaintext = "".join(dec_map[x] for x in ciphertext)
        return {"plaintext": plaintext}


class SubsAtk(Resource):
    def get(self):
        args = subs_atk_parser.parse_args()
        ciphertext = args["ciphertext"]
        mono_counts = Counter(ciphertext)
        bi_counts = Counter(zip(ciphertext, ciphertext[1:]))
        return {
            "mono_letters": list(mono_counts.keys()),
            "mono_values": [x / len(ciphertext) for x in mono_counts.values()],
            "bi_letters": list(map("".join, bi_counts.keys())),
            "bi_values": [x / (len(ciphertext) - 1) for x in bi_counts.values()],
        }
