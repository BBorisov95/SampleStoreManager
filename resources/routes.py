from resources.allowed_countries import Countries, CountiesCreate, CountiesUpdate
from resources.authenticator import RegisterUser, LoginUser
from resources.items import (
    CreateItem,
    DeleteItem,
    GetItem,
    GetItemsFromCategory,
    UpdateItem,
    RestockItems,
    UpdateSpecs,
)
from resources.orders import PlaceOrder

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (CreateItem, "/management/item/create-item"),
    (DeleteItem, "/management/item/delete-item/<int:item_id>"),
    (UpdateItem, "/management/item/update-item"),
    (UpdateSpecs, "/data-entry/item/update-item-spec"),
    (RestockItems, "/management/items/restock"),
    (GetItem, "/item/get-item/<int:item_id>"),
    (GetItemsFromCategory, "/items/category/<string:category_name>"),
    (Countries, "/show-countries"),
    (CountiesCreate, "/management/create-country"),
    (CountiesUpdate, "/management/update-country-taxes"),
    (PlaceOrder, "/item/purchase"),
)
