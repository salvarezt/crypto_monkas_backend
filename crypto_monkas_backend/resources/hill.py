from flask_restful import Resource, reqparse, abort
from typing import List, Tuple
import numpy as np
import cv2
from sys import path
import os
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
    det = np.linalg.det(key)
    if det % 3 == 0 or det % 5 == 0 or det % 17 == 0:
        raise ValueError("Argument is not invertible")
    return key


def valid_format(name: str) -> bool:
    name = name.split(".")
    return name[-1] in ["jpg", "png"]


hill_enc_parser = utils.file_parser()

hill_dec_parser = utils.file_parser()


class HillEnc(Resource):
    def post(self, filename: str, key: str):
        print(filename, key)
        try:
            key = hill_key(key)
        except ValueError as error:
            abort(400, message=error)
        if not valid_format(filename):
            abort(400, message="Unvalid File Format")
        args = hill_enc_parser.parse_args()
        image_file = args['file'].read()
        image_file = np.fromstring(image_file, np.uint8)
        image_file = cv2.imdecode(image_file, cv2.IMREAD_UNCHANGED)
        cv2.imwrite(utils.FILEPATH + filename, image_file)
        self.encryption(filename, key)
        with open(utils.FILEPATH + filename, "rb") as ciphertext:
            ciphertext = base64.b64encode(ciphertext.read()).decode()
        return {"ciphertext": ciphertext}

    @staticmethod
    def encryption(filename: str, key: np.matrix) -> str:
        image = cv2.imread(utils.FILEPATH + filename)
        height, width, _ = image.shape
        kheight, kwidth = key.shape
        dimensions = (width // kwidth * kwidth, height // kheight * kheight)
        image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
        print(image.shape)
        color_channels = cv2.split(image)
        new_channels = []
        for channel in color_channels:
            print(channel.shape)
            for i in range(0, channel.shape[0], kheight):
                for j in range(0, channel.shape[1], kwidth):
                    print(i, j)
                    channel[i: i + kheight, j: j + kwidth] = np.matmul(channel[i: i + kheight, j: j + kwidth], key)
            new_channels.append(channel)
        image = cv2.merge(new_channels)
        cv2.imwrite(utils.FILEPATH + filename, image)


class HillDec(Resource):
    def post(self, filename: str, key: str):
        try:
            key = hill_key(key)
        except ValueError as error:
            abort(400, message=error)
        if not valid_format(filename):
            abort(400, message="Unvalid File Format")
        args = hill_enc_parser.parse_args()
        image_file = args['file']
        image_file.save(filename)

    @staticmethod
    def decryption(filename: str, key: int) -> str:
        pass
