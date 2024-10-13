from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import ProductionConfig, DevelopmentConfig
from db import db
from resources.routes import routes

environment = config("working_env")
if environment == "dev":
    environment = DevelopmentConfig
else:
    environment = ProductionConfig

app = Flask(__name__)
app.config.from_object(environment)

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


@app.teardown_appcontext
def close_request(response):
    db.session.commit()

    return response


[api.add_resource(*route) for route in routes]

if __name__ == "__main__":
    app.run(debug=True)
