
1) [Example Endpoints](#example-endpoints)
   1) [Register](#register)
   2) [Login](#login)
   3) [Create Item](#create-item)
   4) [Delete Item](#delete-item)
   5) [Get Item](#get-item)
   6) [Get Item From Category](#get-items-from-category)
   7) [Update Fields](#update-fields)
   8) [Items restock](#items-restock)
   9) [Spec Update](#spec-update)

## Example endpoints

### Register

Will make new record in db. Return logged user auth. token

url_endpoint: `http://127.0.0.1:5000/register`

method: `POST`
access: `public`


example payload:
```json
{
"username": "user",
"password": "Valid@$$w0rd",
"first_name": "User",
"last_name": "One",
"email": "useroe@user.com"
    }
```

Expected response:

1) Valid:
```json

{
    "token": "auth token"
}
```
2) Invalid:
```json
{
    "message": "Invalid payload {error info}"
}
```
--
### Login

Authorize the user. Will assign token

url_endpoint: `http://127.0.0.1:5000/login`

method: `POST`

access: `public`


example payload:
```json
{
    "username":"user1",
    "password":"Valid@$$w0rd"
}
```

Expected response:

1) Valid:
```json

{
    "token": "auth token"
}
```
2) Invalid:
```json
{
    "message": "Invalid payload {error info}"
}
```
---
### Create item

Will create new record in db

Url_endpoint: `http://127.0.0.1:5000/management/create-item`

method: `POST`

access: `private` Only managers can access this resource


example payload:
```json
{
    "name": "Item7",
    "price": 31231.123,
    "part_number": "p7",
    "ean": "1234567891011",
    "category": "",
    "specs": {},
    "stocks":2
}

```

Expected response:

1) Valid:
```json
{
    "item": {
        "name": "Item7",
        "price": 31231.123,
        "part_number": "p7",
        "ean": 1234567891011.0,
        "category": "",
        "specs": {}
    }
}
```
2) Invalid: -> `HTTP 409`

---

### Delete item

Requires manager roles.

url_endpoint: `http://127.0.0.1:5000/management/item/delete-item/<int: item_id>`

method: `POST`

access: `private`


Expected Responses
1) Valid: `HTTP 204` 
2) Invalid `NotFound`

---

### Get Item

Each User.Role will see different output item fields.

url_endpoint = `http://127.0.0.1:5000/item/get-item/7`

method: `GET`

access: `private`. Every logged user can access this resource. With limited field view.


Expected responses:

1) Valid:
```json
{
    "item": {
        "name": "",
        "part_number": "p4",
        "ean": "1234567891011",
        "price": 201.0,  # dispatcher will not see this field
        "category": "test2",  # dispatcher will not see this field
        "specs": {}, # dispatcher will not see this field
        "id": 7,  # only manager & dispatcher will see this field
        "stocks": 2,   # only manager will see this field
        "sold_pieces": 0  # only manager will see this field
    }
}
```
2) Invalid -> `NotFound`

---

### Get Items from category


url_endpoint: `http://127.0.0.1:5000/item/category/test2`

method: `get`

access: `private` Every logged user can access this resource with limited field view mentored at `Get Item`.

Similar to [Get Item](#get-item) but will return multiple object in an array:

```json
{"{category_name}_items":[item1, item2]}
```

---

### Update Fields

Used to update item fields. Except `specs` and `restock`

url_endpoint: `management/item/update-item`

`method`: `put`

`access`: `private` Only managers can access this resource

The payload must have valid `prod_id`, also optional other ItemModel fields.
Example payload:
```json
{
 "prod_id": 7, # required
 "part_number": "pt7" #optional     
}

```

Expected responses: `201`, `403` or `404` if `prod_id` is not valid.

---

### Items restock

Used to increase the wherehouse stock of items.
Can pass bulk of items at once. Making it possible to update multiple products.


`url_endpoint`: `http://127.0.0.1:5000/management/items/restock`

`method`: `put`

`access`: `private` Only managers can access this resource

Expected payload:

```json

{
   "items":
    [
       {
          "prod_id": 7,
          "stock": 10
       },
       {
          "prod_id": 5,
          "stock": 10
       }
    ]
}

```

Return `201` if successful or `404` if prod_id is not valid.


---

### Spec Update

Spec update endpoint is used to extract specs from 3rd party provider `IceCat`.
The requested specs will overwrite all existing field value for `name`, `part_number`, `category`
Will add json like values into column `specs`.


`url_endpoint`: `http://127.0.0.1:5000/data-entry/item/update-item-spec`
`method`: `post`  -> Limited only for `data_entry` role users.

Example payload:
```json
{
    "brand": "Samsung",
    "product_code": "EV-NX500ZBMHDE",
    "ean": "",
    "use_paid_account": ["",""],
    "internal_prod_id": 5
    
}
```

Expected output:

1) Valid -> json response with `kvp`
2) Invalid -> Different STRING information about 3p provider status: `TimeOutError`, `change_ean`, `Full IceCat Required`
---