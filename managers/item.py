from werkzeug import exceptions as werkzeug_exceptions
from werkzeug.exceptions import NotFound
from db import db
from models import ItemModel
from utils.db_handler import do_commit


class ItemManager:
    """
    Handle the ItemModel related options
    """

    @staticmethod
    def create_item(item_data: dict):
        item = ItemModel(**item_data)
        do_commit(item)
        return item

    @staticmethod
    def delete_item(item_id: int):
        """
        Delete record from db
        :param item_id:
        :return: None
        """
        requested_item = db.session.execute(
            db.select(ItemModel).filter_by(id=item_id)
        ).scalar()
        if not requested_item:
            ItemManager.raises_common_errors(NotFound, raises_for="item")
        db.session.delete(requested_item)
        db.session.flush()

    @staticmethod
    def update_specs(item_id: str):
        """
        Trigger IceCat API endpoint to get specs
        :param item_id:
        :return: updated spec value of item in db
        """
        ...

    @staticmethod
    def update_item_fields(data_to_change: dict):
        """
        Handle the logic of updating any files except specs
        :return: None
        """
        requested_item_id = data_to_change.get("prod_id")
        requested_item = db.session.execute(
            db.select(ItemModel).filter_by(id=requested_item_id)
        ).scalar()
        if not requested_item:
            ItemManager.raises_common_errors(NotFound, raises_for="item")
        del data_to_change[
            "prod_id"
        ]  # renamed schema's id field to prod_id to not shallow build in id
        data_to_change["id"] = requested_item_id
        db.session.bulk_update_mappings(ItemModel, [data_to_change])
        db.session.flush()

    @staticmethod
    def restock(data: dict):
        """
        Increase/decrease product quantity on stock
        :param data: item data
        :return: none -> updated stock value of item
        """
        for item in data.get("items"):
            item_to_restock = ItemManager.get_item(item.get("prod_id"))
            item_to_restock.stocks += item.get("stock")
        db.session.flush()

    @staticmethod
    def get_item(item_id: int):
        """
        Get specific item information
        :param item_id: item_id
        :return:
        """
        item = db.session.execute(db.select(ItemModel).filter_by(id=item_id)).scalar()

        if not item:
            ItemManager.raises_common_errors(NotFound, "item")
        if item.stocks <= 0:
            raise NotFound("The requested item is currently not available for sale!")

        return item

    @staticmethod
    def get_all_items_from_cat(cat_name: str):
        """
        Get specific category item catalog
        :param cat_name: category name
        :return:
        """
        items = (
            db.session.execute(db.select(ItemModel).filter_by(category=cat_name))
            .scalars()
            .all()
        )

        if not items:
            ItemManager.raises_common_errors(NotFound, "category")

        return items

    @staticmethod
    def raises_common_errors(error_to_raise: werkzeug_exceptions, raises_for: str):
        if raises_for == "item":
            raise error_to_raise("The item which you search is not existing!")
        if raises_for == "category":
            raise error_to_raise(
                "The requested category does not exist or does not contain items!"
            )
