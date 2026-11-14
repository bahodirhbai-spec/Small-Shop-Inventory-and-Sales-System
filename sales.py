import json
import os

import numpy as np

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from storage import load_products, save_products
from inventory import reduce_stock, list_product


SALES_FILE = "sales.json"
LOW_STOCK_LIMIT = 5


# ==========================================
# PYDANTIC MODEL
# ==========================================

class Sale(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    sale_id: str = Field(pattern=r"^S\d{4,}$")
    product_id: str = Field(pattern=r"^P\d{4,}$")
    product_name: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: int = Field(gt=0)
    total: int = Field(gt=0)


# ==========================================
# LOAD SALES
# ==========================================

def load_sales():
    """sales.json dan sotuvlarni o'qiydi va Pydantic orqali tekshiradi."""

    if not os.path.exists(SALES_FILE):
        return []

    try:
        with open(SALES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (json.JSONDecodeError, OSError):
        # Jim bo'sh ro'yxat qaytarmaymiz: keyingi saqlashda eski
        # sotuvlar o'chib ketmasligi uchun xatoni ochiq ko'rsatamiz.
        raise ValueError(
            "sales.json faylini o'qib bo'lmadi. Faylni tekshiring."
        )

    if not isinstance(data, list):
        raise ValueError("sales.json fayli ro'yxat bo'lishi kerak.")

    validated_sales = []

    for index, sale in enumerate(data, start=1):
        try:
            validated_sales.append(Sale.model_validate(sale).model_dump())

        except ValidationError as error:
            raise ValueError(
                f"sales.json faylidagi {index}-sotuv noto'g'ri:\n{error}"
            )

    return validated_sales


# ==========================================
# SAVE SALES
# ==========================================

def save_sales(sales):
    """Sotuvlarni Pydantic orqali tekshirib JSON faylga yozadi."""

    validated_sales = [
        Sale.model_validate(sale).model_dump()
        for sale in sales
    ]

    temp_file = SALES_FILE + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(
            validated_sales,
            file,
            ensure_ascii=False,
            indent=4
        )

    os.replace(temp_file, SALES_FILE)


# ==========================================
# GENERATE SALE ID
# ==========================================

def generate_sale_id(sales):
    """S0001, S0002, ... ko'rinishida keyingi sotuv ID sini qaytaradi."""

    numbers = []

    for sale in sales:
        sid = str(sale.get("sale_id", ""))

        if sid.startswith("S") and sid[1:].isdigit():
            numbers.append(int(sid[1:]))

    next_number = max(numbers) + 1 if numbers else 1

    return "S" + str(next_number).zfill(4)


# ==========================================
# MAKE SALE (input() yo'q: (True, sale) yoki (False, xato matni))
# ==========================================

def make_sale(product_id, quantity):
    """Bitta mahsulotni sotadi: zaxirani kamaytiradi va sotuvni saqlaydi.

    Rad etilgan sotuv zaxirani ham, sotuvlar tarixini ham o'zgartirmaydi.
    """

    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        return False, "Miqdor noldan katta butun son bo'lishi kerak."

    product_id = str(product_id).strip().upper()
    product = None

    for item in load_products():
        if item["id"] == product_id:
            product = item
            break

    if product is None:
        return False, "Bunday ID dagi mahsulot topilmadi."

    if product["stock"] < quantity:
        return False, (
            f"Zaxira yetarli emas. Omborda: {product['stock']} dona."
        )

    sales = load_sales()

    try:
        sale = Sale(
            sale_id=generate_sale_id(sales),
            product_id=product["id"],
            product_name=product["name"],
            quantity=quantity,
            unit_price=product["price"],          # sotuv paytidagi narx
            total=product["price"] * quantity
        ).model_dump()

    except ValidationError as error:
        return False, f"Sotuv ma'lumotlari noto'g'ri:\n{error}"

    # Zaxirani inventory.py orqali kamaytiramiz
    if not reduce_stock(product["id"], quantity):
        return False, "Zaxirani kamaytirib bo'lmadi."

    sales.append(sale)

    try:
        save_sales(sales)

    except OSError:
        # Sotuv saqlanmadi: zaxirani avvalgi holatiga qaytaramiz
        products = load_products()

        for item in products:
            if item["id"] == product["id"]:
                item["stock"] += quantity

        save_products(products)

        return False, "Sotuvni saqlab bo'lmadi. Zaxira qayta tiklandi."

    return True, sale


# ==========================================
# RECORD SALE (menyu uchun, input() bilan)
# ==========================================

def record_sale():
    """Mahsulot va miqdorni so'rab, sotuvni yozadi."""

    products = load_products()

    if not products:
        print("Omborda maxsulot mavjud emas, sotuv qilib bo'lmaydi!")
        return None

    list_product()

    product_id = input("\nSotiladigan mahsulot ID raqami: ").strip().upper()

    if not any(product["id"] == product_id for product in products):
        print("Xato! Bunday ID dagi mahsulot topilmadi.")
        return None

    while True:
        quantity = input("Nechta dona sotiladi?  ").strip()

        if quantity.isdecimal() and int(quantity) > 0:
            quantity = int(quantity)
            break

        print("Xato! Noldan katta butun son kiriting!")

    ok, result = make_sale(product_id, quantity)

    if not ok:
        print(f"Sotuv rad etildi: {result}")
        return None

    print(
        f"Sotuv yozildi: {result['quantity']} x {result['product_name']} "
        f"= {result['total']:,} UZS"
    )

    return result


# ==========================================
# LIST SALES
# ==========================================

def list_sales():
    """Sotuvlar tarixini jadval ko'rinishida chiqaradi."""

    sales = load_sales()

    if not sales:
        print("\nHozircha sotuvlar yo'q")
        return sales

    print("\n" + "=" * 86)
    print(
        f"{'№':<4} | {'Sotuv':<8} | {'Mahsulot':<20} | {'Soni':<6} | "
        f"{'Narxi (UZS)':<12} | {'Jami (UZS)':<12}"
    )
    print("=" * 86)

    for number, sale in enumerate(sales, start=1):
        print(
            f"{number:<4} | "
            f"{sale['sale_id']:<8} | "
            f"{sale['product_name']:<20} | "
            f"{sale['quantity']:<6} | "
            f"{sale['unit_price']:<12,} | "
            f"{sale['total']:<12,}"
        )

    print("=" * 86)

    return sales


# ==========================================
# REPORTS
# ==========================================

def total_revenue():
    """Barcha sotuvlarning umumiy tushumi (sotuv bo'lmasa 0)."""

    return sum(sale["total"] for sale in load_sales())


def best_selling_product():
    """Eng ko'p sotilgan mahsulot: (nomi, soni) yoki None."""

    totals = {}

    for sale in load_sales():
        pid = sale["product_id"]

        if pid not in totals:
            totals[pid] = {"name": sale["product_name"], "quantity": 0}

        totals[pid]["quantity"] += sale["quantity"]

    if not totals:
        return None

    best = max(totals.values(), key=lambda item: item["quantity"])

    return best["name"], best["quantity"]


def low_stock_products():
    """Zaxirasi 5 yoki undan kam bo'lgan mahsulotlar ro'yxati."""

    return [
        product for product in load_products()
        if product["stock"] <= LOW_STOCK_LIMIT
    ]


def average_sale_amount():
    """NumPy bilan o'rtacha sotuv summasi; sotuv bo'lmasa None."""

    sales = load_sales()

    if not sales:
        return None

    totals = np.array([sale["total"] for sale in sales], dtype=np.int64)

    return float(np.mean(totals))


def show_reports():
    """Hisobotlarni chiqaradi."""

    print("\n" + "-" * 45)
    print("                 HISOBOTLAR")
    print("-" * 45)

    print(f"Umumiy tushum:         {total_revenue():,} UZS")

    best = best_selling_product()

    if best is None:
        print("Eng ko'p sotilgan:     sotuvlar yo'q")
    else:
        print(f"Eng ko'p sotilgan:     {best[0]} ({best[1]} dona)")

    average = average_sale_amount()

    if average is None:
        print("O'rtacha sotuv:        sotuvlar yo'q")
    else:
        print(f"O'rtacha sotuv:        {round(average):,} UZS")

    if not load_products():
        print("Kam qolgan mahsulotlar: omborda maxsulot yo'q")

    else:
        low = low_stock_products()

        if not low:
            print("Kam qolgan mahsulotlar: yo'q (hammasida 5 dan ko'p)")
        else:
            print(f"Kam qolgan mahsulotlar ({LOW_STOCK_LIMIT} va undan kam):")

            for product in low:
                print(
                    f"  {product['id']} - {product['name']}: "
                    f"{product['stock']} dona"
                )

    print("-" * 45)