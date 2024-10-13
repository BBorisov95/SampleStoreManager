from flask import request
from flask_restful import Resource

from managers.user import UserManager
from schemas.request.user import UserRegisterSchema, UserLoginSchema
from utils.decorators import validate_schema


class RegisterUser(Resource):
    @validate_schema(UserRegisterSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.create_user(data)
        return {"token": token}, 201


class LoginUser(Resource):
    @validate_schema(UserLoginSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {"token": token}, 200
