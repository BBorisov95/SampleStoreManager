
1) [Example Endpoints](#example-endpoints)
   1) [Register](#register)
   2) [Login](#login)
   3) [Create Item](#create-item)
   4) [Delete Item](#delete-item)
   5) [Get Item](#get-item)
   6) [Get Item From Category](#get-items-from-category)

## Example endpoints

### Register

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
## Login

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
## Create item


Url_endpoint: `http://127.0.0.1:5000/management/create-item`

method: `POST`

access: `private`


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

## Delete item

Requires manager roles.

url_endpoint: `http://127.0.0.1:5000/management/item/delete-item/<int: item_id>`

method: `POST`

access: `private`


Expected Responses
1) Valid: `HTTP 204` 
2) Invalid `NotFound`

---

## Get Item

Each User.Role will see different output item fields.

url_endpoint = `http://127.0.0.1:5000/item/get-item/7`

method: `GET`

access: `private`


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

## Get Items from category


url_endpoint: `http://127.0.0.1:5000/item/category/test2`

method: `post`

access: `private`

Similar to [Get Item](#get-item) but will return multiple object in an array:

```json
{"{category_name}_items":[item1, item2]}
```