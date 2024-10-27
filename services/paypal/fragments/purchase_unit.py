class PurchaseUnit:
    """
    This is like the purchase receipt which the customer will see:
    Total value, internal reference to the order
    items: [item1, item2]
    """

    units = set()

    def __init__(self, builder):
        """
        Set product instance
        :param builder: builder instance
        """
        self.currency_code: str = builder.currency_code
        self.value: float = builder.value
        self.reference_id: int = builder.reference_id
        self.items: list[dict] = builder.items
        PurchaseUnit.units.add(self)

    def to_dict(self):
        """Convert the PurchaseUnit instance to a dictionary."""
        total_value = str(round(self.value, 2))
        return {
            "reference_id": str(self.reference_id),
            "items": self.items,
            "amount": {
                "currency_code": str(self.currency_code),
                "value": total_value,
                "breakdown": {
                    "item_total": {
                        "currency_code": str(self.currency_code),
                        "value": total_value,
                    },
                },
            },
        }

    def __repr__(self):
        return str(self.to_dict())
