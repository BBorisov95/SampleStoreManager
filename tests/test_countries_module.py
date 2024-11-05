from copy import deepcopy

from models import CountryModel
from models.enums import UserRole
from tests.base_functionalities import APIBaseTestCase
from tests.factories import CountryFactory


class TestCountryModule(APIBaseTestCase):
    """
    Suit for testing Countries manager & endpoints behavior
    """

    def make_requests(self, data: dict, expected_msg: str, headers: dict):
        resp = self.client.post(
            "/management/create-country", json=data, headers=headers
        )
        self.assert400(resp)
        self.assertEqual(resp.json["message"], expected_msg)

    def test_get_all_countries(self):
        """
        Get all allowed countries
        """

        for _ in range(5):
            CountryFactory()

        all_countries: list[str] = [c.country_name for c in CountryModel.query.all()]
        for user_role in UserRole:
            resp = self.client.get(
                "/show-countries", headers=self.return_user_headers(for_role=user_role)
            )
            for country in all_countries:
                self.assertIn(
                    country,
                    resp.json["countries"].get("allowed_countries_to_deliver").keys(),
                )
            self.assert200(resp)

    def test_country_create_and_update_schema(self):
        """
        Test failure of endpoint if not
        """
        data: dict = {
            "country_name": "Greece",
            "prefix": "GRC",
            "regular_delivery_price": 15,
            "fast_delivery_price": 22.9,
            "express_delivery_price": 65.99,
            "currency": "EURO",
        }

        headers: dict = self.return_user_headers(UserRole.manager)

        initial_countries: list[CountryModel] = CountryModel.query.all()
        self.assertEqual(len(initial_countries), 0)

        # missing country name
        invalid_country_name: dict = deepcopy(data)
        del invalid_country_name["country_name"]
        expected_msg = (
            "Invalid payload {'country_name': ['Missing data for required field.']}"
        )
        self.make_requests(
            data=invalid_country_name, expected_msg=expected_msg, headers=headers
        )

        # missing prefix
        invalid_prefix: dict = deepcopy(data)
        del invalid_prefix["prefix"]
        expected_msg = (
            "Invalid payload {'prefix': ['Missing data for required field.']}"
        )
        self.make_requests(
            data=invalid_prefix, expected_msg=expected_msg, headers=headers
        )

        # invalid prices
        invalid_prices: dict = deepcopy(data)
        invalid_prices["regular_delivery_price"] = -1
        invalid_prices["fast_delivery_price"] = -1
        invalid_prices["express_delivery_price"] = -1
        expected_msg = (
            "Invalid payload {'regular_delivery_price': ['Invalid value.'], "
            "'fast_delivery_price': ['Invalid value.'], 'express_delivery_price': "
            "['Invalid value.']}"
        )
        self.make_requests(
            data=invalid_prices, expected_msg=expected_msg, headers=headers
        )

        # invalid currency to short

        invalid_currency: dict = deepcopy(data)
        invalid_currency["currency"] = "AB"
        expected_msg = "Invalid payload {'currency': ['Invalid value.']}"
        self.make_requests(
            data=invalid_currency, expected_msg=expected_msg, headers=headers
        )

        # invalid currency to long
        invalid_currency["currency"] = "ABCDEFG"
        self.make_requests(
            data=invalid_currency, expected_msg=expected_msg, headers=headers
        )

    def test_create_and_update_country_successfully(self):
        """
        Check the behavior when valid data is passed.
        """

        data: dict = {
            "country_name": "Greece",
            "prefix": "GRC",
            "regular_delivery_price": 15,
            "fast_delivery_price": 22.9,
            "express_delivery_price": 65.99,
            "currency": "EURO",
        }

        all_countries: list[CountryModel] = CountryModel.query.all()
        self.assertEqual(len(all_countries), 0)

        headers = self.return_user_headers(UserRole.manager)
        resp = self.client.post(
            "/management/create-country", headers=headers, json=data
        )
        self.assertEqual(resp.status_code, 201)

        all_countries: list[CountryModel] = CountryModel.query.all()
        self.assertEqual(len(all_countries), 1)

        # test update (same schema and logic)
        data["regular_delivery_price"] = 0
        update_resp = self.client.put(
            "/management/update-country-taxes", headers=headers, json=data
        )
        self.assertEqual(update_resp.status_code, 201)

        check_country_changed_status: CountryModel = CountryModel.query.filter_by(
            country_name=data["country_name"]
        ).scalar()
        self.assertEqual(check_country_changed_status.regular_delivery_price, 0)
