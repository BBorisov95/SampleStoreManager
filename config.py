from decouple import config


class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('db_user')}:{config('db_pass')}"
        f"@{config('db_host')}:{config('db_port')}/{config('db_name')}"
    )


class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('db_user')}:{config('db_pass')}"
        f"@{config('db_host')}:{config('db_port')}/{config('db_name')}"
    )
