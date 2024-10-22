from db import db
from models.country import CountryModel
from utils.db_handler import do_commit

from werkzeug.exceptions import NotFound


class CountryManager:

    @staticmethod
    def get_delivery_tax(country: str, delivery_type: str) -> float:
        """
        Return the predefined cost for delivery per country per delivery type
        :param country: Country to deliver
        :param delivery_type: Delivery type
        :return: the tax for delivery
        """

        country: CountryModel = db.session.execute(
            db.select(CountryModel).filter_by(country_name=country)
        ).scalar()
        if not country:
            raise NotFound("Invalid country!")
        delivery_type = delivery_type + "_delivery_price"
        if hasattr(country, delivery_type):
            return getattr(country, delivery_type)

    @staticmethod
    def get_all_allowed_countries(return_only_country_name: bool = False) -> list:
        """
        Return a list of tuples
        :return: list of tuples [(country, prefix)] | [Country_name,...]
        """
        if return_only_country_name:
            all_countries = db.session.execute(
                (db.select(CountryModel.country_name))
            ).scalars()
        else:
            """
            If specific multiple columns we use all()
            """
            all_countries = db.session.execute(
                db.select(CountryModel.country_name, CountryModel.prefix)
            ).all()

        return all_countries

    @staticmethod
    def create_new_country(country_create_data: dict):
        """
        Create new country info
        :return: None
        """
        new_country = CountryModel(**country_create_data)
        do_commit(new_country)

    @staticmethod
    def update_delivery_taxes(new_taxes: dict):
        """
        Update country records
        :param new_taxes: new records data
        :return: None or 404
        """
        country: db.Model = db.session.execute(
            db.select(CountryModel).filter_by(
                country_name=new_taxes.get("country_name")
            )
        ).scalar()
        if country:
            country.regular_delivery_price = new_taxes.get(
                "regular_delivery_price", country.regular_delivery_price
            )
            country.fast_delivery_price = new_taxes.get(
                "fast_delivery_price", country.fast_delivery_price
            )
            country.express_delivery_price = new_taxes.get(
                "express_delivery_price", country.express_delivery_price
            )
            db.session.flush()
        else:
            raise NotFound("Country not found in db records!")
