from flask_restful import Resource, reqparse
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


def head_value(value: str) -> int:
    value = value.split(" ")
    try:
        value = int(value[0])
    except ValueError:
        raise ValueError("Argument can't be parse as integer")
    if value <= 0 or 26 < value:
        raise ValueError("Argument out of range of possibilities")
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
subs_atk_parser.add_argument(
    "head", type=head_value, required=True, help="unvalid_argument: {error_msg}"
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
        pass
