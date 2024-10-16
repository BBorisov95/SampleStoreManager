from flask import request
from flask_restful import Resource

from managers.authenticator import auth
from managers.item import ItemManager
from models.enums import UserRole
from schemas.request.item import (
    ItemCreationSchema,
    ItemUpdateSchema,
    ItemListRestocksSchema,
)
from schemas.response.item import (
    ItemResponseSchema,
    ItemResponseManagersSchema,
    ItemResponseDispatcherSchema,
)
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


class GetItemsFromCategory(Resource):
    @auth.login_required
    def get(self, category_name: str):
        user = auth.current_user()

        requested_items_from_category = ItemManager.get_all_items_from_cat(
            category_name
        )

        if user.role == UserRole.regular:
            return {
                f"{category_name}_items": ItemResponseSchema().dump(
                    requested_items_from_category, many=True
                )
            }, 200
        if user.role == UserRole.manager:
            return {
                f"{category_name}_items": ItemResponseManagersSchema().dump(
                    requested_items_from_category, many=True
                )
            }, 200
        if user.role == UserRole.dispatcher:
            return {
                f"{category_name}_items": ItemResponseDispatcherSchema().dump(
                    requested_items_from_category, many=True
                )
            }, 200


class UpdateItem(Resource):

    @auth.login_required
    @permission_required(UserRole.manager)
    @validate_schema(ItemUpdateSchema)
    def put(self):
        data = request.get_json()
        ItemManager.update_item_fields(data)
        return {}, 201


class RestockItems(Resource):
    @auth.login_required
    @permission_required(UserRole.manager)
    @validate_schema(ItemListRestocksSchema)
    def put(self):
        data = request.get_json()
        ItemManager.restock(data)
        return {}, 201
