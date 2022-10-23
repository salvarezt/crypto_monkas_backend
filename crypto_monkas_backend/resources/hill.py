from flask_restful import Resource, abort
import numpy as np
from sympy.matrices import Matrix
from sympy.matrices.dense import matrix2numpy
from PIL import Image
from sys import path
import base64

path.append("../common")

from common import utils


def hill_key(key: str):
    key = "".join([c if (c.isdecimal() or c.isspace()) else "" for c in key])
    key = list(map(int, key.split()))
    match len(key):
        case 4:
            size = 2
            pass
        case 9:
            size = 3
            pass
        case 16:
            size = 4
            pass
        case _:
            raise ValueError("Wrong Argument size")
    key = np.matrix([key[i: i + size] for i in range(0, len(key), size)])
    det = Matrix(key).det()
    if det % 256 == 0:
        raise ValueError("Argument is not invertible")
    return key


def valid_format(name: str) -> bool:
    name = name.split(".")
    return name[-1] in ["jpg", "png"]


hill_enc_parser = utils.file_parser()

hill_dec_parser = utils.file_parser()


class HillEnc(Resource):
    def post(self, filename: str, key: str):
        try:
            key = hill_key(key)
        except ValueError as error:
            abort(400, message=error)
        if not valid_format(filename):
            abort(400, message="Unvalid File Format")
        args = hill_enc_parser.parse_args()
        image_file = args["file"]
        image_file.save(utils.FILEPATH + filename)
        self.encryption(filename, key)
        with open(utils.FILEPATH + "encimg" + filename, "rb") as ciphertext:
            ciphertext = base64.b64encode(ciphertext.read()).decode()
        return {"ciphertext": ciphertext}

    @staticmethod
    def encryption(filename: str, key: np.matrix) -> str:
        image = Image.open(utils.FILEPATH + filename)
        height, width = image.size
        kheight, kwidth = key.shape
        dimensions = (height // kheight * kheight, width // kwidth * kwidth)
        image = image.resize(dimensions)
        image = np.array(image)
        print(image[:kheight, :kwidth, 0])
        for channel in range(3):
            for i in range(0, image.shape[0], kheight):
                for j in range(0, image.shape[1], kwidth):
                    image[i: i + kheight, j: j + kwidth, channel] = np.matmul(
                            image[i: i + kheight, j: j + kwidth, channel], key
                    ) % 256
        image = Image.fromarray(image)
        image.save(utils.FILEPATH + "encimg" + filename)


class HillDec(Resource):
    def post(self, filename: str, key: str):
        try:
            key = hill_key(key)
        except ValueError as error:
            abort(400, message=error)
        if not valid_format(filename):
            abort(400, message="Unvalid File Format")
        args = hill_enc_parser.parse_args()
        image_file = args["file"]
        image_file.save(utils.FILEPATH + filename)
        self.decryption(filename, key)
        with open(utils.FILEPATH + "decimg" + filename, "rb") as plaintext:
            plaintext = base64.b64encode(plaintext.read()).decode()
        return {"plaintext": plaintext}

    @staticmethod
    def decryption(filename: str, key: int) -> str:
        invkey = Matrix(key).inv_mod(256)
        invkey = matrix2numpy(invkey)
        image = Image.open(utils.FILEPATH + filename)
        height, width = image.size
        kheight, kwidth = key.shape
        dimensions = (height // kheight * kheight, width // kwidth * kwidth)
        image = image.resize(dimensions)
        image = np.array(image)
        for channel in range(3):
            for i in range(0, image.shape[0], kheight):
                for j in range(0, image.shape[1], kwidth):
                    image[i: i + kheight,j: j + kwidth, channel] = np.matmul(
                        image[i: i + kheight, j: j + kwidth, channel], invkey
                    ) % 256
        image = Image.fromarray(image)
        image.save(utils.FILEPATH + "decimg" + filename)
