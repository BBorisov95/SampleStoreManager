from flask import request
from flask_restful import Resource

from managers.authenticator import auth
from managers.item import ItemManager
from models.enums import UserRole
from schemas.request.item import ItemCreationSchema
from schemas.response.item import ItemResponseSchema, ItemResponseManagersSchema, ItemResponseDispatcherSchema
from utils.decorators import permission_required, validate_schema


class CreateItem(Resource):

    @auth.login_required
    @permission_required(UserRole.manager)
    @validate_schema(ItemCreationSchema)
    def post(self):
        item_data = request.get_json()
        item = ItemManager.create_item(item_data)
        return {"item": ItemResponseSchema().dump(item)}, 201


class DeleteItem(Resource):
    @auth.login_required
    @permission_required(UserRole.manager)
    def delete(self, item_id: int):
        ItemManager.delete_item(item_id)
        return {}, 204


class GetItem(Resource):
    @auth.login_required
    def get(self, item_id: int):
        user = auth.current_user()

        requested_item = ItemManager.get_item(item_id)

        if user.role == UserRole.regular:
            return {"item": ItemResponseSchema().dump(requested_item)}, 200
        if user.role == UserRole.manager:
            return {"item": ItemResponseManagersSchema().dump(requested_item)}, 200
        if user.role == UserRole.dispatcher:
            return {"item": ItemResponseDispatcherSchema().dump(requested_item)}, 200
