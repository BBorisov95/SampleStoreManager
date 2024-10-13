from resources.authenticator import RegisterUser, LoginUser
from resources.items import CreateItem, DeleteItem, GetItem, GetItemsFromCategory

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (CreateItem, "/management/item/create-item"),
    (DeleteItem, "/management/item/delete-item/<int:item_id>"),
    (GetItem, "/item/get-item/<int:item_id>"),
    (GetItemsFromCategory, "/item/category/<string:category_name>")
)
