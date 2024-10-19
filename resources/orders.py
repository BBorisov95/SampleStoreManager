from flask import request
from flask_restful import Resource

from managers.authenticator import auth
from managers.order import OrderManager
from models.user import UserModel
from schemas.request.order import OrderPlaceSchema
from schemas.response.order import OrderResponseSchema
from utils.decorators import validate_schema


class PlaceOrder(Resource):

    @auth.login_required
    @validate_schema(OrderPlaceSchema)
    def post(self):
        data: dict = request.get_json()
        current_user: UserModel = auth.current_user()
        order: OrderManager = OrderManager.place_order(current_user, data)
        return {"order": OrderResponseSchema().dump(order)}, 201
