from resources.authenticator import RegisterUser, LoginUser
from resources.items import CreateItem

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (CreateItem, "/management/create-item"),
)
