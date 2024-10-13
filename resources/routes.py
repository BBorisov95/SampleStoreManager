from resources.authenticator import RegisterUser, LoginUser
from resources.items import CreateItem, DeleteItem

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (CreateItem, "/management/item/create-item"),
    (DeleteItem, "/management/item/delete-item/<int:item_id>")
)
