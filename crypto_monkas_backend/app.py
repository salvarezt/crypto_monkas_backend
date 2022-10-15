from flask import Flask
import os
from flask_restful import Api
from resources.shift import ShiftEnc, ShiftDec, ShiftAtk
from resources.afin import AfinAtk, AfinDec, AfinEnc
from resources.substitution import SubsEnc, SubsDec, SubsAtk
from resources.vigenere import VigEnc, VigDec, VigAtk
from resources.permutation import PermEnc, PermDec
from resources.hill import HillEnc

TMP = "./resources/tmp"

if os.path.exists(TMP):
    for file_path in os.listdir(TMP):
        try:
            os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
else:
    os.makedirs(TMP)

app = Flask(__name__)
app.config['UPLOAD FOLDER'] = TMP

api = Api(app)

api.add_resource(ShiftEnc, "/shift/enc")
api.add_resource(ShiftDec, "/shift/dec")
api.add_resource(ShiftAtk, "/shift/atk")
api.add_resource(AfinEnc, "/afin/enc")
api.add_resource(AfinDec, "/afin/dec")
api.add_resource(AfinAtk, "/afin/atk")
api.add_resource(SubsEnc, "/subs/enc")
api.add_resource(SubsDec, "/subs/dec")
api.add_resource(SubsAtk, "/subs/atk")
api.add_resource(VigEnc, "/vig/enc")
api.add_resource(VigDec, "/vig/dec")
api.add_resource(VigAtk, "/vig/atk")
api.add_resource(PermEnc, "/perm/enc")
api.add_resource(PermDec, "/perm/dec")
api.add_resource(HillEnc, "/hill/enc")

if __name__ == "__main__":
    app.run(debug=True)
