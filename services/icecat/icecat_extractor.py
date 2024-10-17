import requests
from requests.exceptions import ConnectionError, Timeout


class IceCatExtractor:

    def __init__(self, brand: str, product_code: str, ean: int or None = None, use_paid_account: bool = False, *args, **kwargs):
        self.s: requests = requests.Session()
        self.use_paid_account = use_paid_account
        self.user_name: str = self.use_paid_account[0]
        if self.use_paid_account:
            self.s.auth = (self.user_name, self.use_paid_account[1])
        self.brand: str = brand
        self.prod_id: str = product_code
        self.ean: str = ean
        self.api_url: str = (
            f"https://live.icecat.biz/api?"
            f"UserName={self.user_name}&"
            f"Language=en&Brand={self.brand}&"
            f'{"ProductCode" if self.prod_id else "GTIN"}'
            f"={self.prod_id if self.prod_id else self.ean}"
        )

    @property
    def user_name(self):
        return self.__user_name

    @user_name.setter
    def user_name(self, value):
        value = value.strip()
        if not value:
            self.__user_name = 'openIcecat'
            self.use_paid_account = False
        else:
            self.__user_name = value

    def do_request(self):
        try:
            response = self.s.get(url=self.api_url)
            json_response = response.json()
        except (
            ConnectionError,
            Timeout,
        ):

            print(f"Timeout for {self.api_url}")
            return "TimeOutError"

        if json_response.get("Code") is not None:
            with open("failed_requests.txt", "a+") as f:
                f.write(
                    f'{self.brand} -> {self.ean if self.ean else self.prod_id} ----->> {json_response.get("Message")},\n'
                )
            if "The GTIN can not be found" in json_response.get("Message"):
                return "change_ean"
            if (
                "Full Icecat subscription level will require the use"
                in json_response.get("Message")
            ):
                return "Full IceCat Required"

        if json_response:
            return self.extract_json_response_info(json_response)


    def extract_json_response_info(self, json_object: dict):
        json_obj_general_info = json_object.get("data").get("GeneralInfo")
        ice_cat_category = (
            json_obj_general_info.get("Category").get("Name").get("Value")
        )
        brand = json_obj_general_info.get("Brand")
        model = json_obj_general_info.get("BrandPartCode")
        ean = json_obj_general_info.get("GTIN")
        product_name = json_obj_general_info.get("TitleInfo").get("GeneratedIntTitle")
        ice_cat_specs = {
            "Brand": brand,
            "Model": model,
            "ean": ean,
            "name": product_name,
            "category": ice_cat_category
        }

        if ice_cat_category == "Laptops":
            series = json_obj_general_info.get("ProductName")
            ice_cat_specs.update({"Series": series, "Model": model})

        for spec_dict in json_object.get("data").get("FeaturesGroups"):
            """
            loop over all spec groups
            """
            for spec in spec_dict.get("Features"):
                """
                loop over specs in the group
                """
                value = spec.get("Value", None)
                spec_name = (
                    spec.get("Feature", None).get("Name", None).get("Value", None)
                )

                ice_cat_specs.update({spec_name: value})

        return ice_cat_specs
