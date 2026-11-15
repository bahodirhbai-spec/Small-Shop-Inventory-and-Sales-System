from inventory import (
    add_product,
    find_product,
    get_product,
    inventory_value,
    list_product,
    reduce_stock,
    restock_product,
)

from sales import list_sales, record_sale, show_reports


def main():
    while True:
        print("\n" + "=" * 45)
        print("       SMALL SHOP INVENTORY SYSTEM")
        print("=" * 45)

        print("1. Add Product")
        print("2. List Products")
        print("3. Find Product")
        print("4. Get Product by ID")
        print("5. Restock Product")
        print("6. Reduce Stock")
        print("7. Inventory Total Value")
        print("8. Record Sale")
        print("9. Sales History")
        print("10. Reports")
        print("0. Exit")

        print("=" * 45)

        try:
            choose = input("Choose an option: ").strip()

            if choose == "1":
                add_product()

            elif choose == "2":
                list_product()

            elif choose == "3":
                product = find_product()
                if product:
                    print("\nProduct Found:")
                    print(product)

            elif choose == "4":
                product = get_product()
                if product:
                    print("\nProduct Details:")
                    print(product)

            elif choose == "5":
                restock_product()

            elif choose == "6":
                product_id = input(
                    "Enter Product ID (masalan P0002 yoki 2, "
                    "0 - bekor qilish): "
                ).strip()

                if product_id in ("", "0"):
                    print("Bekor qilindi.")
                    continue

                while True:
                    qty = input(
                        "Enter quantity to reduce (0 - bekor qilish): "
                    ).strip()

                    if qty in ("", "0"):
                        print("Bekor qilindi.")
                        qty = None
                        break

                    if qty.isdigit() and int(qty) > 0:
                        qty = int(qty)
                        break

                    print("Error! Enter a positive integer.")

                if qty is None:
                    continue

                if reduce_stock(product_id, qty):
                    print("Stock successfully reduced!")
                else:
                    print("Error! Product not found or insufficient stock.")

            elif choose == "7":
                total = inventory_value()

                print("\n" + "-" * 35)
                print(f"Total Inventory Value: {total:,} UZS")
                print("-" * 35)

            elif choose == "8":
                record_sale()

            elif choose == "9":
                list_sales()

            elif choose == "10":
                show_reports()

            elif choose == "0":
                print("\nThank you for using Inventory System!")
                break

            else:
                print("\nInvalid option! Please choose again.")

        except (KeyboardInterrupt, EOFError):
            print("\n\nDastur to'xtatildi.")
            break

        except (ValueError, OSError) as error:
            print(f"\nXato: {error}")


if __name__ == "__main__":
    main()
