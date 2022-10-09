from flask import Flask
from flask_restful import Api
from resources.shift import ShiftEnc, ShiftDec, ShiftAtk
from resources.afin import AfinAtk, AfinDec, AfinEnc
from resources.substitution import SubsEnc, SubsDec, SubsAtk

app = Flask(__name__)
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

if __name__ == "__main__":
    app.run(debug=True)
