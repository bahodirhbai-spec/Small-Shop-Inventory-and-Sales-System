"""Mahsulotlarni saqlash uchun moslik (compatibility) qatlami.

Asosiy kod endi inventory.py da. Bu fayl eski importlar buzilmasligi
uchun o'sha funksiyalarni qayta eksport qiladi.
"""

from inventory import (
    PRODUCTS_FILE,
    Product,
    load_products,
    normalize_product_id,
    save_products,
)


__all__ = [
    "PRODUCTS_FILE",
    "Product",
    "load_products",
    "normalize_product_id",
    "save_products",
]
