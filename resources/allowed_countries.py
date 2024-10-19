"""
This file is like a mapper for which countries we can deliver
Will be exposed to endpoint
"""

from flask_restful import Resource

from schemas.response.allowed_countries import AllowedCountriesResponseSchema

ALLOWED_COUNTRIES = {"bulgaria": "bgr", "greece": "grc"} # TODO DB!


class ShowCountries(Resource):

    def get(self):
        formatted_countries = {
            country.title(): code.upper() for country, code in ALLOWED_COUNTRIES.items()
        }

        response = AllowedCountriesResponseSchema().dump({
            "allowed_countries_to_deliver": formatted_countries
        })
        return {
            "countries": response


        }, 200
