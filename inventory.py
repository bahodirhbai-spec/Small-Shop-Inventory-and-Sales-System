
import json
import os

import numpy as np

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


# ==========================================
# GENERATE PRODUCT ID
# ==========================================

def generate_product_id(products):
    """P0001, P0002, ... ko'rinishida keyingi ID ni qaytaradi."""

    numbers = []

    for product in products:
        pid = str(product.get("id", ""))

        if pid.startswith("P") and pid[1:].isdigit():
            numbers.append(int(pid[1:]))

    next_number = max(numbers) + 1 if numbers else 1

    return "P" + str(next_number).zfill(4)


# ==========================================
# ADD PRODUCT
# ==========================================

def add_product(quentity=None, id=None, name=None, price=None, stock=None):
    """Yangi mahsulot qo'shadi va Pydantic orqali tekshiradi."""

    while True:
        quentity = input("Nechta maxsulot kiritmoqchisiz ?   ").strip()

        if quentity.isdigit() and int(quentity) > 0:
            break

        print("Xato! Noldan katta bo'lgan raqam kiriting: ")

    quentity = int(quentity)
    products = load_products()
    added_ids = []

    for number in range(1, quentity + 1):
        print("\n" + str(number) + "- maxsulot")

        while True:
            name = input("Maxsulot nomini kiriting: ").strip()

            if name != "":
                break

            print("Xato! Iltimos qaytadan maxsulot nomini kiriting: ")

        while True:
            price = input("Narxi (UZS): ").strip()

            if price.isdigit() and int(price) > 0:
                break

            print("Xato! Narx noldan katta butun son bo'lishi kerak: ")

        while True:
            stock = input("Ombordagi miqdori:  ").strip()

            if stock.isdigit():
                break

            print("Xato! Miqdor butun son bo'lishi kerak (0 ham bo'lishi mumkin):  ")

        product_id = generate_product_id(products)

        try:
            product = Product(
                id=product_id,
                name=name,
                price=int(price),
                stock=int(stock)
            )

            products.append(product.model_dump())
            added_ids.append(product_id)

        except ValidationError as error:
            print("Product validation error:")
            print(error)

    save_products(products)

    return True, added_ids


# ==========================================
# LIST PRODUCT
# ==========================================

def list_product():
    """Barcha mahsulotlarni jadval ko'rinishida chiqaradi."""

    products = load_products()

    if not products:
        print("\nOmborda hozircha maxsulot yoq")
        return products

    print("\n" + "=" * 70)
    print(f"{'ID':<10} | {'Nomi':<20} | {'Narxi (UZS)':<12} | {'Zaxira':<6}")
    print("=" * 70)

    for product in products:
        price = int(product["price"])
        stock = int(product["stock"])

        print(
            f"{product['id']:<10} | "
            f"{product['name']:<20} | "
            f"{price:<12,} | "
            f"{stock:<6}"
        )

    print("=" * 70)

    return products


# ==========================================
# FIND PRODUCT
# ==========================================

def find_product():
    """ID yoki nom bo'yicha mahsulot qidiradi."""

    products = load_products()

    if not products:
        print("Omborda maxsulot mavjud emas!")
        return None

    while True:
        query = input(
            "Iltimos maxsulot ID yoki nomini kiriting:  "
        ).strip()

        if query != "":
            for product in products:

                if (
                    query.upper() == product["id"]
                    or query.lower() in product["name"].lower()
                ):
                    return product

        print("Xato! Maxsulot topilmadi, Iltimos qaytadan kiriting:  ")


# ==========================================
# GET PRODUCT
# ==========================================

def get_product():
    """ID bo'yicha aniq mahsulotni topadi."""

    products = load_products()

    if not products:
        print("Omborda mahsulot mavjud emas!")
        return None

    while True:
        product_id = input(
            "Mahsulot ID raqamini kiriting: "
        ).strip().upper()

        for product in products:

            if product_id == product["id"]:
                return product

        print("Xato! Bunday ID dagi mahsulot topilmadi. Qaytadan kiriting!")


# ==========================================
# RESTOCK PRODUCT
# ==========================================

def restock_product():
    """Tanlangan mahsulot zaxirasini oshiradi."""

    products = load_products()

    if not products:
        print("Omborda maxsulot mavjud emas!")
        return None

    while True:
        product_id = input(
            "Iltimos maxsulot ID raqamini kiriting:  "
        ).strip().upper()

        selected = None

        for product in products:

            if product["id"] == product_id:
                selected = product
                break

        if selected is not None:
            break

        print("Xato! Bunday ID dagi mahsulot topilmadi. Qaytadan kiriting!")

    while True:
        add_stock = input(
            "Zaxiraga yana nechta qo'shmoqchisiz ?   "
        ).strip()

        if add_stock.isdigit() and int(add_stock) > 0:
            break

        print("Xato! Noldan katta butun son kiriting!")

    try:
        updated_product = Product(
            **{
                **selected,
                "stock": int(selected["stock"]) + int(add_stock)
            }
        )

        selected.update(updated_product.model_dump())

    except ValidationError as error:
        print("Product validation error:")
        print(error)
        return None

    save_products(products)

    print("Tabriklayman, Zaxira muvaffaqiyatli yangilandi")

    return selected


# ==========================================
# REDUCE STOCK
# ==========================================

def reduce_stock(product_id, qty):
    """Mahsulot zaxirasini kamaytiradi."""

    products = load_products()

    if not products:
        return False

    if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
        return False

    for product in products:

        if product_id.strip().upper() == product["id"].upper():

            current_stock = int(product["stock"])

            if current_stock < qty:
                return False

            try:
                updated_product = Product(
                    **{
                        **product,
                        "stock": current_stock - qty
                    }
                )

                product.update(updated_product.model_dump())

            except ValidationError:
                return False

            save_products(products)

            return True

    return False


# ==========================================
# INVENTORY VALUE
# ==========================================

def inventory_value():
    """Ombordagi barcha mahsulotlarning umumiy qiymatini hisoblaydi."""

    products = load_products()

    if not products:
        return 0

    prices = np.array(
        [int(product["price"]) for product in products],
        dtype=np.int64
    )

    stocks = np.array(
        [int(product["stock"]) for product in products],
        dtype=np.int64
    )

    total_value = np.sum(prices * stocks)

    return int(total_value)
