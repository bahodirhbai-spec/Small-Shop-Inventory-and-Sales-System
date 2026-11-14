import json
import os

from pydantic import BaseModel, ConfigDict, Field, ValidationError


PRODUCTS_FILE = "products.json"


# ==========================================
# PYDANTIC MODEL
# ==========================================

class Product(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    id: str = Field(pattern=r"^P\d{4,}$")
    name: str = Field(min_length=1)
    price: int = Field(gt=0)
    stock: int = Field(ge=0)


# ==========================================
# LOAD PRODUCTS
# ==========================================

def load_products():
    """products.json dan mahsulotlarni o'qiydi va Pydantic orqali tekshiradi."""

    if not os.path.exists(PRODUCTS_FILE):
        return []

    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    validated_products = []

    for index, product in enumerate(data, start=1):
        try:
            validated_product = Product.model_validate(product)
            validated_products.append(validated_product.model_dump())

        except ValidationError as error:
            raise ValueError(
                f"products.json faylidagi {index}-mahsulot noto'g'ri:\n{error}"
            )

    return validated_products


# ==========================================
# SAVE PRODUCTS
# ==========================================

def save_products(products):
    """Mahsulotlarni Pydantic orqali tekshirib JSON faylga yozadi."""

    validated_products = [
        Product.model_validate(product).model_dump()
        for product in products
    ]

    with open(PRODUCTS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            validated_products,
            file,
            ensure_ascii=False,
            indent=4
        )