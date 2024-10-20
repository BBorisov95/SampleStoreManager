import re

from werkzeug.exceptions import BadRequest

from schemas.validators.empty_string_checker import is_empty_string
from managers.country import CountryManager


def validate_country(country: str):
    """
    Validate if the country is in the allowed for selling
    :param country: requested country
    :return: raises BadRequest or None
    """
    is_empty_string(country, "Country")
    allowed_countries = CountryManager.get_all_allowed_countries(
        return_only_country_name=True
    )
    if country.title() not in list(allowed_countries):
        raise BadRequest(
            f'Sorry we cannot deliver your order to {country}. Currently we can deliver only to: {",".join([c.title() for c in allowed_countries])}'
        )


def validate_city(city: str):
    """
    Validates if city is passed as param
    :param city: requested city
    :return: raises or none
    """
    is_empty_string(city, "City")


def validate_postal_code(postal_code: str):
    """
    Validate if postal_code is in desired format
    future validate the postal code
    :param postal_code: requested postal code in specific format country_prefix:code
    :return: raises or none
    """
    is_empty_string(postal_code, "Postal Code")

    try:
        prefix, code = postal_code.split(":")
        is_valid = re.findall(r"\d+", code)
        if not is_valid:
            raise BadRequest(f"Postal Code is not valid!")
    except ValueError:
        raise BadRequest(
            f"Invalid postal code format. Required type is COUNTRY_PREFIX:POSTAL_CODE."
            f" List of prefixes can be found here: /show-countries "
        )
