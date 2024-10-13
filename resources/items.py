from flask import request
from flask_restful import Resource

from managers.authenticator import auth
from managers.item import ItemManager
from models.enums import UserRole
from schemas.request.item import ItemCreationSchema
from schemas.response.item import ItemResponseSchema
from utils.decorators import permission_required, validate_schema


class CreateItem(Resource):

    @auth.login_required
    @permission_required(UserRole.manager)
    @validate_schema(ItemCreationSchema)
    def post(self):
        item_data = request.get_json()
        item = ItemManager.create_item(item_data)
        return {"item": ItemResponseSchema().dump(item)}, 201
