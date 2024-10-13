


## Example endpoints

### Register

Url_endpoint: `http://127.0.0.1:5000/register`

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

Url_endpoint: `http://127.0.0.1:5000/login`

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

--