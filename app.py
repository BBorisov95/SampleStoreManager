from decouple import config

from config import ProductionConfig, DevelopmentConfig
from config import create_app
from db import db

environment = config("working_env")
if environment == "dev":
    environment = DevelopmentConfig
else:
    environment = ProductionConfig

app = create_app(environment)


@app.teardown_appcontext
def close_request(response):
    db.session.commit()

    return response


if __name__ == "__main__":
    app.run(debug=True)
