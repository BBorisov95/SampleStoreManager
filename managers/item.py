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
            raise NotFound("The item which you search is not existing!")
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
    def restock(item_id: str, pcs: int):
        """
        Increase/decrease product quantity on stock
        :param item_id: item id
        :param pcs: negative or positive number
        :return: updated stock value of item
        """

    @staticmethod
    def get_item(item_id: str):
        """
        Get specific item information
        :param item_id: item_id
        :return:
        """
        item = db.session.execute(db.select(ItemModel).filter_by(id=item_id)).scalar()

        if not item:
            raise NotFound("The item which you search is not existing!")
        if item.get("stock") <= 0:
            raise NotFound("The requested item is currently not available for sale!")

        a = 5  # TODO CHECK WHAT AND HOW TO RETURN

    @staticmethod
    def get_all_items_from_cat(cat_name: str):
        """
        Get specific category item catalog
        :param cat_name: category name
        :return:
        """
        items = db.session.execute(
            db.select(ItemModel).filter_by(id=cat_name)
        ).scalars()

        if not items:
            raise NotFound(
                "The requested category does not exist or does not contain items!"
            )

        a = 5  # TODO CHECK WHAT AND HOW TO RETURN
