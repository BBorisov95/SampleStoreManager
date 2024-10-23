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
        requested_item: ItemModel = ItemManager.get_item(item_id)
        if not requested_item:
            ItemManager.raises_common_errors(NotFound, raises_for="item")
        db.session.delete(requested_item)
        db.session.flush()

    @staticmethod
    def update_specs(item_id: int, spec_dict: dict):
        """
        Trigger IceCat API endpoint to get specs
        :param item_id: internal product id
        :param spec_dict: dict of specs
        :return: updated spec value of item in db
        """
        requested_item: ItemModel = ItemManager.get_item(item_id)
        if not requested_item:
            ItemManager.raises_common_errors(NotFound, raises_for="item")
        try:
            ean = spec_dict.get("ean")
            if isinstance(ean, list):
                """
                ean is returned as str or None
                """
                ean = ean[0]
            del spec_dict["ean"]  # no need to be in specs as well
            category = spec_dict.get("category")
            del spec_dict["category"]  # no need to be in specs
            name = spec_dict.get("name")
            del spec_dict["name"]  # no need to be in specs
            part_number = spec_dict.get("Model")
            del spec_dict["Model"]
            if ean:
                requested_item.ean = ean
            if category:
                requested_item.category = category
            if name:
                requested_item.name = name
            if part_number:
                requested_item.part_number = part_number

            requested_item.specs = spec_dict
            do_commit(requested_item)
            return requested_item
        except KeyError as ke:
            raise KeyError(f"Invalid data received: {str(ke)}")

    @staticmethod
    def update_item_fields(data_to_change: dict):
        """
        Handle the logic of updating any files except specs
        :return: None
        """
        requested_item_id = data_to_change.get("prod_id")
        requested_item: ItemModel = ItemManager.get_item(requested_item_id)
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
            item_to_restock = ItemManager.get_item(
                item.get("prod_id"), for_restock=True
            )
            item_to_restock.stocks += item.get("stock")
        db.session.flush()

    @staticmethod
    def get_item(item_id: int, for_restock: bool = False):
        """
        Get specific item information
        :param item_id: item_id
        :param for_restock: Bool if True return item even if it's 0 stock
        :return:
        """
        item: ItemModel = db.session.execute(
            db.select(ItemModel).filter_by(id=item_id)
        ).scalar()

        if not item:
            ItemManager.raises_common_errors(NotFound, "item")

        if item.stocks <= 0 and not for_restock:
            raise NotFound("The requested item is currently not available for sale!")

        return item

    @staticmethod
    def get_item_price(item_id: int):
        """
        Get product price
        :param item_id: product_id
        :return: product price -> float
        """
        item: ItemModel = ItemManager.get_item(item_id)

        if not item:
            ItemManager.raises_common_errors(NotFound, "item")

        return item.price

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
    def increase_sold_pcs(item_obj: ItemModel, sold_pcs: int):
        """
        Increase the sold pcs of the itm_obj
        :param item_obj: ItemModel object
        :param sold_pcs: number of sold pcs
        :return: None
        """
        item_obj.sold_pieces += sold_pcs
        do_commit(item_obj)

    @staticmethod
    def raises_common_errors(error_to_raise: werkzeug_exceptions, raises_for: str):
        if raises_for == "item":
            raise error_to_raise("The item which you search is not existing!")
        if raises_for == "category":
            raise error_to_raise(
                "The requested category does not exist or does not contain items!"
            )
