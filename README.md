The project simulate `ERP` like system. Where we can create items. Enrichment them using 3th party provided. Order them and deliver them.
The paymant system is `PayPal` 3th party service. And all order statuses are beign notified using `Discord` services.

One order can contain one or more products.
Each ordered product is stored into `Client Basket` where we can get the needed information whenever we need. 

All changes related to `PayPal`, `Orders`, or `Items` are stored into log table, which makes the tracking of an issue more easly.

---
1) [Endpoints](#endpoints)
   1) [Register](#register)
   2) [Login](#login)
   3) [Create Item](#create-item)
   4) [Delete Item](#delete-item)
   5) [Get Item](#get-item)
   6) [Get Item From Category](#get-items-from-category)
   7) [Update Fields](#update-fields)
   8) [Items restock](#items-restock)
   9) [Spec Update](#spec-update)
   10) [Orders](#orders)
   11) [Countries](#counties)
2) [IceCat](#icecat)
3) [Discord](#discord)
4) [PayPal](#paypal)
5) [Project Setup Guide](#project-setup-guide)

## Endpoints

### Register

Will make new record in db. Return logged user auth. token


| Method  | Access | Endpoint | Required Headers  |
|---------|--------|----------|-------------------|
| GET     | Public |`/register`| `application/json`|

<details> 
    <summary> Example Payload </summary>

```json
{
  "username": "user",
  "password": "Valid@$$w0rd",
  "first_name": "User",
  "last_name": "One",
  "email": "useroe@user.com"
}
```
</details>

<details> 
    <summary> Expected response </summary>

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

</details>


---
### Login

Authorize the user. Will assign token


| Method | Access | Endpoint | Required Headers  |
|-------|--------|----------|-------------------|
| POST  | Public | `/login` | `application/json`|

<details> 
    <summary>Example Payload</summary>

```json
{
  "username":"UserName",
  "password":"Password"
}
```

</details>

<details> 
    <summary>Example Response</summary>


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

</details>

---
### Create item

Accessing this endpoint with the right credentials and payload will create a new Item in the DataBase.


| Method | Access  | Endpoint | Required Headers                              | Additional Restrictions                                 |
|-------|---------|----------|-----------------------------------------------|---------------------------------------------------------|
| POST  | Private | `/management/item/create-item` | `application/json`<br/>`Authorization Bearer` | Only users with role `mangers` <br/>can access this endpoint |


<details>
    <summary> Example Payload </summary>

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
</details>

<details>
    <summary> Expected response </summary>

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

</details>

---

### Delete item

Hitting this endpoint will trigger a process for deleting items from DataBase.


| Method | Access  | Endpoint                                      | Params                    | Required Headers | Additional Restrictions                                 |
|-------|---------|-----------------------------------------------|---------------------------|------------------|------------------------------------------------------|
| POST  | Private | `/management/item/delete-item/<int: item_id>` | Item identification numer |  `application/json`<br/>`Authorization Bearer` | Only users with role `mangers` <br/>can access this endpoint |


<details>
    <summary> Expected response </summary>

1) Valid: `HTTP 204`

2) Invalid `NotFound`
</details>

---

### Get Item

Accessing the endpoint wil results of displaying a product information. 
The retrieved information is truncated based on the user's role 

| Method | Access  | Endpoint                        | Params                    | Required Headers | 
|--------|---------|---------------------------------|---------------------------|------------------|
| GET    | Private | `/item/get-item/<int: item_id>` | Item identification numer |  `application/json`<br/>`Authorization Bearer` |


<details>
    <summary>Additional Restrictions </summary>

| User Role | Will not see                                                 |
|-----------|--------------------------------------------------------------|
| **Dispatcher**  | - price<br>- category<br>- specs<br>- stock<br>- sold pieces |
| **Regular Users**| - id<br>- sold pieces<br>- stock                             |
| **Data Entry**  | - sold pieces<br>- stock                                     |

</details>

<details>
    <summary> Expected response </summary>

1) Valid:
```json
{
    "item": {
        "name": "",
        "part_number": "p4",
        "ean": "1234567891011",
        "price": 201.0,
        "category": "test2",
        "specs": {}, 
        "id": 7,
        "stocks": 2,
        "sold_pieces": 0
    }
}
```
2) Invalid -> `NotFound` Raised when no product found!

</details>

---

### Get Items from category


Similar to [Get Item](#get-item) but will return multiple object in an array. The same restrictions are applied.

| Method | Access  | Endpoint                  | Params        | Required Headers | 
|--------|---------|---------------------------|---------------|------------------|
| GET    | Private | `/items/category/<string:category_name>` | Category name |  `application/json`<br/>`Authorization Bearer` |

<details>
    <summary> Expected response </summary>

```json
{"{category_name}_items":[item1, item2]}
```
</details>

---

### Update Fields

This resource is used to update item fields. Except `specs` and `restock`!


| Method | Access  | Endpoint                  | Required Headers | Additional Restrictions                       |
|--------|---------|---------------------------|------------------|---------------------------------------|
| PUT    | Private | `/management/item/update-item` |  `application/json`<br/>`Authorization Bearer` | Only `Mangers` can access this field! |


The payload must have valid `prod_id`, also optional other `ItemModel` fields.
<details>
    <summary> Example payload </summary>

Where `prod_id` is required and `part_number` is optional

```json
{
 "prod_id": 7,
 "part_number": "pt7"  
}

```
</details>

<details>
    <summary> Expected responses </summary>

1) On Valid response: `201`, `403`.
2) Invalid response will raise`404` if `prod_id` is not valid.

</details>

---

### Items restock

Used to increase the warehouse stock of items. Can pass bulk of items at once. Making it possible to update multiple products.


| Method | Access  | Endpoint                  | Required Headers | Additional Restrictions                       |
|--------|---------|---------------------------|------------------|---------------------------------------|
| PUT    | Private | `/management/items/restock` |  `application/json`<br/>`Authorization Bearer` | Only `Mangers` can access this field! |


<details>
    <summary>Expected payload</summary>


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

</details>


<details>
    <summary>Expected response</summary>

1) On valid requests:`201`.
2) If requests is not Valid: `404`.
</details>


---

### Spec Update

Spec update endpoint is used to extract specs from 3rd party provider `IceCat`.
The requested specs will overwrite all existing field value for `name`, `part_number`, `category`
Will add json like values into column `specs`.

Check more about `IceCat` -> [IceCat](#icecat)

---

### Orders

The following section describe the orders endpoints and how to be used.

1) PlaceOrder

Triggering this endpoint will create orders in the system. An order must have at least one item and valid delivery address.

| Method | Access  | Endpoint                  | Required Headers | Additional Restrictions |
|--------|---------|---------------------------|------------------|-------------------------|
| POST   | Private | `/item/purchase` |  `application/json`<br/>`Authorization Bearer` | Only logged users.      |


<details>
    <summary>Example Payload</summary>

```json
{
  "items": [
    {
        "prod_id": 1,
        "quantity": 1
    },
    {
        "prod_id": 25,
        "quantity": 1
    }
  ],
   "delivery_address": {
        "to_country": "Bulgaria",
        "to_city": "Sofia",
        "to_zipcode": "BGR:1000",
        "to_street_address": "Opulchenska",
        "to_building_number": 6
   },
   "delivery_type": "regular"
}
```
</details>


<details>
    <summary>Expected Responses</summary>

  1) Valid
   ```json
   {
       "order": {
           "id": 57,
           "status": "Waiting to process the order.",
           "delivery_type": "From 4 to 5 days",
           "payment_status": "The order is not paid!",
           "total_order": 31432.123
       }
   }
   ```
   2) Invalid:
   
   An order can be invalid if any of the items are invalid.
   
  ```json
   {
       "message": "The item which you search is not existing!"
   }

   ```

   Or if the ` "delivery_address": {
           "to_country": }}` is not valid. (Check [Countries](#counties) )
   
   Return a json info msg.
   ```json
   {
       "message": "Sorry we cannot deliver your order to Costa Ricka. Currently we can deliver only to: Bulgaria, Greece"
   }
   ```
</details>


2) Get orders

Get the logged user all successfully placed orders. Including the order details.


| Method | Access  | Endpoint                  | Required Headers | Additional Restrictions |
|--------|---------|---------------------------|------------------|-------------------------|
| GET    | Private | `/get-orders` |  `application/json`<br/>`Authorization Bearer` | Only logged users.      |


<details>
    <summary>Expected response</summary>

```json
{
    "all_orders": [
        {
            "id": 59,
            "delivery_to" : {},
            "status": "Waiting to process the order.",
            "delivery_type": "From 4 to 5 days",
            "payment_status": "The order is not paid!",
            "total_order": 31432.123
        },
        {
            "id": 60,
            "delivery_to" : {},
            "status": "Waiting to process the order.",
            "delivery_type": "From 2 to 3 days",
            "payment_status": "The order is not paid!",
            "total_order": 31432.123
        },
        {
            "id": 61,
            "delivery_to" : {},
            "status": "Waiting to process the order.",
            "delivery_type": "Next day delivery",
            "payment_status": "The order is not paid!",
            "total_order": 31432.123
        }
    ]
}
```

</details>

---

### Counties

Allowed countries are the places which we can operate on. An order can be placed only in these countries.
Everyone can access this endpoints

Each country has `name` and `prefix`


| Method | Access | Endpoint                  | Required Headers |
|--------|--------|---------------------------|------------------|
| GET    | Public | `show-countries` |  `application/json`<br/>|

<details>
    <summary>Expected Response</summary>

```json
{
    "countries": {
        "allowed_countries_to_deliver": {
            "Bulgaria": "BGR",
            "Greece": "GRC"
        }
    }
}
```

</details>

---

### Create Country

Create a new country where the system can operate. Here we set the currency and the prices for the different type of deliveries.

| Method | Access  | Endpoint                  | Required Headers | Additional Restrictions                       |
|--------|---------|---------------------------|------------------|---------------------------------------|
| POST   | Private | `/management/create-country` |  `application/json`<br/>`Authorization Bearer` | Only `Mangers` can access this field! |

<details>
    <summary>Example payload</summary>

```json
{
    "country_name": "Greece",
    "prefix": "GRC",
    "regular_delivery_price": 10,
    "fast_delivery_price": 20,
    "express_delivery_price": 45.99,
    "currency": "EURO"
}
```

</details>

<details>
    <summary>Expected Response </summary>

A valid requests will return HTTP Status code: `201`

</details>

---
### Update Country delivery Taxes

Used when the there is a need to update a country delivery fees.

| Method | Access  | Endpoint                  | Required Headers | Additional Restrictions                       |
|--------|---------|---------------------------|------------------|---------------------------------------|
| PUT    | Private | `/management/update-country-taxes` |  `application/json`<br/>`Authorization Bearer` | Only `Mangers` can access this field! |

<details>
    <summary>Example payload </summary>

The same schema as <i>Create Country</i>

```json

{
    "country_name": "Greece",
    "prefix": "GRC",
    "regular_delivery_price": 15,
    "fast_delivery_price": 25.9,
    "express_delivery_price": 65.99,
    "currency": "EURO"
}

```
</details>

<details>
    <summary> Expected Response</summary>

A valid request will return HTTP Status Code: `201`
</details>


---

### IceCat

IceCat module is used by DataEntry (UserRole) and has the rights to update the product fields and append specs.

`url_endpoint`: `/data-entry/item/update-item-spec`

`method`: `PUT`

`access`: `private` Only users with dole data_entry can access it.


| Method | Access  | Endpoint                  | Required Headers | Additional Restrictions                  |
|--------|---------|---------------------------|------------------|------------------------------------------|
| POST   | Private | `/data-entry/item/update-item-spec` |  `application/json`<br/>`Authorization Bearer` | Only `Data Entry` can access this field! |

<details>
    <summary>Example payload</summary>

Where `use_paid_account` is tuple with private credentials `tuple(user_name: str, password: str)`. If provided can access larger database access from IceCat.
Otherwise only free access is provided.

```json
{
    "brand": "Samsung",
    "product_code": "EV-NX500ZBMHDE",
    "ean": "",
    "use_paid_account": ["",""],
    "internal_prod_id": 5
    
}
```


</details>

<details>
    <summary> Expected response </summary>

1) Valid -> `json` response with `kvp`
```json
{
    "message": "Item with id 10 is updated by data entry",
    "specs": {
        "name": "Haier HCE233S freezer",
        "part_number": "HCE233S",
        "ean": "6930265374711",
        "price": 55.99,
        "category": "Freezers",
        "specs": {
            "Brand": "Haier",
            ...
        },
        "last_update_by": 1,
        "id": 10
    }
}
```

2) Invalid -> Different STRING information about 3p provider status: `TimeOutError`, `change_ean`, `Full IceCat Required`.

</details>


---

### Discord


Basic script which send messages to chanel regarding order statuses.

`bot_id` and `chanel_id` must be set as env

There is no direct endpoint. It's invoked from the different managers.

---

### PayPal

Simple PayPal integration, which allow payments of an order.

`endpoint`: `/user/order/<int:order_id>/pay`

`method`: `POST`

`access`: `private` 


| Method | Access  | Endpoint                  | Params                      | Required Headers                                | Additional Restrictions                      |
|--------|---------|---------------------------|-----------------------------|-------------------------------------------------|----------------------------------------------|
| POST   | Private | `/user/order/<int:order_id>/pay` | Order identification number |   `application/json`<br/>`Authorization Bearer` | Only Logged user can access this endpoint. Also there is a protection if logged user A try to access order for user B which will raise `Unauthorized(f"Sorry you cannot pay for this order. It's not yours!")`|


When this endpoint is triggerd will send request to `PayPal` to create a transaction / receipt with order details. Including separated products / quantity total price per product.
And final total price.

After that will receive confirm link in the following format `{our_domain}/paypal-redirect/approve?token={}&PayerId={}`
which is a `GET` request and can be handled easy from FE, to open new window with this link. Which will lead the user to his PayPal login screen and `Pay Order` button.

---

# Project Setup Guide

## Prerequisites

Before setting up the project, make sure you have the following installed:

- **PostgreSQL**: You will need to have PostgreSQL installed and running on your system.
- **Python 3.9+**: Python 3.9 or higher must be installed.
- **Flask**:

## Setup Instructions

### For Windows OS

1. **Install PostgreSQL**:
   - Download and install PostgreSQL from [here](https://www.postgresql.org/download/windows/).
   - During installation, ensure that the PostgreSQL bin directory is added to your system's PATH environment variable.

2. **Install Python 3.9+:
   - Download Python 3.9+ from [here](https://www.python.org/downloads/).

3. **Clone the Project Repository**:
   - Open Command Prompt and navigate to the directory where you want to clone the project:
     ```bash
     git clone https://github.com/BBorisov95/SampleStoreManager.git
     cd SampleStoreManager
     ```

4. **Create and Activate Virtual Environment**:
   - Create a virtual environment to isolate project dependencies:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     ```bash
     .\venv\Scripts\activate
     ```

5. **Install Required Packages**:
   - Install all required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

6. **Configure Database**:
   - Set up PostgreSQL database and create a database for your project.
   - Make sure your `SQLALCHEMY_DATABASE_URI` in the config file is set correctly (e.g., `postgresql://username:password@localhost/dbname`).

7. **Run Database Migrations**:
   - Apply the database migrations:
     ```bash
      flask db upgrade
     ```

8. **Run the Flask Application**:
   - Start the Flask development server:
     ```bash
     flask run
     ```
   - Visit `http://127.0.0.1:5000/` to see the application in action.

### For Unix OS (Linux/MacOS)

1. **Install PostgreSQL**:
   - On Ubuntu/Debian-based systems, install PostgreSQL via APT:
     ```bash
     sudo apt update
     sudo apt install postgresql postgresql-contrib
     ```
   - On MacOS, install PostgreSQL via Homebrew:
     ```bash
     brew install postgresql
     ```

2. Install Python 3.9+:
   - On Ubuntu/Debian-based systems, install Python and pip:
     ```bash
     sudo apt install python3.9 python3.9-venv python3.9-dev
     sudo apt install python3-pip
     ```
   - On MacOS, install python following [MiniConda Docs](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)

3. **Clone the Project Repository**:
   - Clone the project from GitHub:
     ```bash
     git clone https://github.com/BBorisov95/SampleStoreManager.git
     cd SampleStoreManager
     ```

4. **Create and Activate Virtual Environment**:
   - Create a virtual environment:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     ```bash
     source venv/bin/activate
     ```

5. **Install Required Packages**:
   - Install dependencies from `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

6. **Configure Database**:
   - Set up PostgreSQL database and create a database for your project.
   - Ensure the `SQLALCHEMY_DATABASE_URI` in your configuration is correct.

7. **Run Database Migrations**:
   - Apply migrations:
     ```bash
      flask db upgrade
     ```

8. **Run the Flask Application**:
   - Start the Flask application:
     ```bash
     flask run
     ```
   - Visit `http://127.0.0.1:5000/` to view the app.
