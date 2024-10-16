from resources.authenticator import RegisterUser, LoginUser
from resources.items import (
    CreateItem,
    DeleteItem,
    GetItem,
    GetItemsFromCategory,
    UpdateItem,
    RestockItems,
)

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (CreateItem, "/management/item/create-item"),
    (DeleteItem, "/management/item/delete-item/<int:item_id>"),
    (UpdateItem, "/management/item/update-item"),
    (RestockItems, "/management/items/restock"),
    (GetItem, "/item/get-item/<int:item_id>"),
    (GetItemsFromCategory, "/items/category/<string:category_name>"),
)
