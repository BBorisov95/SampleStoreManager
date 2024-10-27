"""
This file is like a mapper for which countries we can deliver
Will be exposed to endpoint
"""

from flask import request
from flask_restful import Resource

from managers.authenticator import auth
from managers.country import CountryManager
from models.enums import UserRole
from schemas.request.country import CountryCreateAndUpdateSchema
from schemas.response.allowed_countries import AllowedCountriesResponseSchema
from utils.decorators import validate_schema, permission_required


class Countries(Resource):

    @staticmethod
    def get():
        all_countries = CountryManager.get_all_allowed_countries()

        formatted_countries: dict = {
            country.title(): code.upper() for country, code in all_countries
        }

        response: dict = AllowedCountriesResponseSchema().dump(
            {"allowed_countries_to_deliver": formatted_countries}
        )
        return {"countries": response}, 200


class CountiesCreate(Resource):
    @auth.login_required
    @permission_required(UserRole.manager)
    @validate_schema(CountryCreateAndUpdateSchema)
    def post(self):
        data: dict = request.get_json()
        CountryManager.create_new_country(data)
        return {}, 201


class CountiesUpdate(Resource):

    @auth.login_required
    @permission_required(UserRole.manager)
    @validate_schema(CountryCreateAndUpdateSchema)
    def put(self):
        data: dict = request.get_json()
        CountryManager.update_delivery_taxes(data)
        return {}, 201
