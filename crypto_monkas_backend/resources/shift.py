from flask_restful import Resource, reqparse
from sys import path

path.append("../common")

from common import utils


def shift_key(value: str) -> int:
    value = "".join([c if (c.isdecimal() or c.isspace()) else "" for c in value])
    value = value.split()
    try:
        value = int(value[0]) % 26
    except IndexError:
        raise ValueError("No argument was provided")
    except ValueError:
        raise ValueError("Argument can't be parse as integer")

    return value


def head_value(value: str) -> int:
    value = value.split(" ")
    try:
        value = int(value[0])
    except ValueError:
        raise ValueError("Argument can't be parse as integer")
    if value <= 0 or 26 < value:
        raise ValueError("Argument out of range of possibilities")
    return value


shift_enc_parser = reqparse.RequestParser()
shift_enc_parser.add_argument(
    "plaintext", type=utils.plaintext, required=True, help="plaintext is required"
)
shift_enc_parser.add_argument(
    "key", type=shift_key, required=True, help="unvalid argument: {error_msg}"
)

shift_dec_parser = reqparse.RequestParser()
shift_dec_parser.add_argument(
    "ciphertext", type=utils.ciphertext, required=True, help="ciphertext is required"
)
shift_dec_parser.add_argument(
    "key", type=shift_key, required=True, help="unvalid argument: {error_msg}"
)

shift_atk_parser = reqparse.RequestParser()
shift_atk_parser.add_argument(
    "ciphertext", type=utils.ciphertext, required=True, help="ciphertext is required"
)
shift_atk_parser.add_argument(
    "head", type=head_value, required=True, help="unvalid_argument: {error_msg}"
)


class ShiftEnc(Resource):
    def get(self):
        args = shift_enc_parser.parse_args()
        plaintext = args["plaintext"]
        key = args["key"]
        ciphertext = "".join(
            [utils.chr_up((utils.ascci_code(c) + key) % 26) for c in plaintext]
        )
        return {"ciphertext": ciphertext}


class ShiftDec(Resource):
    def get(self):
        args = shift_dec_parser.parse_args()
        ciphertext = args["ciphertext"]
        key = args["key"]
        plaintext = "".join(
            [utils.chr_low((utils.ascci_code(c) - key) % 26) for c in ciphertext]
        )
        return {"plaintext": plaintext}


class ShiftAtk(Resource):
    def get(self):
        args = shift_atk_parser.parse_args()
        ciphertext = args["ciphertext"]
        head = args["head"]
        plaintexts_keys = [
            ["".join([utils.chr_low((utils.ascci_code(c) - key) % 26) for c in ciphertext]), key]
            for key in range(26)
        ]
        plaintexts, keys = zip(*sorted(plaintexts_keys, key=lambda x: utils.diff_rank(x[0])))
        return {"plaintexts": plaintexts[0:head], "keys": keys[0:head]}
