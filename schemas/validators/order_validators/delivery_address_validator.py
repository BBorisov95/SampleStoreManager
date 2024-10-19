import re

from werkzeug.exceptions import BadRequest

from resources.allowed_countries import ALLOWED_COUNTRIES
from schemas.validators.empty_string_checker import is_empty_string

POSTAL_CODE_MAP_VALIDATORS = {
    "bgr": lambda postal_code: bool(re.match(r"\d{4}", postal_code)),
    #TODO MAKE IT A DB element
}


def validate_country(country: str):
    """
    Validate if the country is in the allowed for selling
    :param country: requested country
    :return: raises BadRequest or None
    """
    is_empty_string(country, "Country")
    if country.lower() not in ALLOWED_COUNTRIES.keys():
        raise BadRequest(
            f'Sorry we cannot deliver your order to {country}. Currently we can deliver only to: {",".join([c.title() for c in ALLOWED_COUNTRIES.keys()])}'
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
        is_valid = POSTAL_CODE_MAP_VALIDATORS[prefix.lower()](code)
        if not is_valid:
            raise BadRequest(f"Postal Code is not valid!")
    except ValueError:
        raise BadRequest(
            f"Invalid postal code format. Required type is COUNTRY_PREFIX:POSTAL_CODE."
            f" List of prefixes can be found here: /show-countries "
        )
