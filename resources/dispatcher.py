from flask import request
from flask_restful import Resource

from managers.authenticator import auth
from managers.dispatcher import DispatcherManager
from models.enums import UserRole
from models.order import OrderModel
from schemas.request.dispatch import DispatchOrderRequestSchema
from schemas.response.dispatch import DispatchOrderResponseSchema
from utils.decorators import validate_schema, permission_required


class DispatchItem(Resource):

    @auth.login_required
    @permission_required(UserRole.dispatcher)
    @validate_schema(DispatchOrderRequestSchema)
    def post(self):
        """
        Post requests will send this data
        :return:
        """
        data: dict = request.get_json()
        DispatcherManager.dispatch_item(order_data=data)


class GetOrdersForDispatch(Resource):

    @auth.login_required
    @permission_required(UserRole.dispatcher)
    def get(self):
        """
        Get all orders with status NEW
        and "prepare" for collection
        :return: List of orders
        """
        all_orders: list[OrderModel] = DispatcherManager.get_all_orders_for_dispatch()
        return {
            "all_order_for_dispatch": DispatchOrderResponseSchema().dump(
                all_orders, many=True
            )
        }, 200
