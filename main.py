from inventory import add_product, list_product,  find_product, get_product, restock_product, reduce_stock, inventory_value


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
        print("0. Exit")

        print("=" * 45)

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
            product_id = input("Enter Product ID: ").strip()
            
            while True:
                qty = input("Enter quantity to reduce: ").strip()

                if qty.isdigit() and int(qty) > 0:
                    qty = int(qty)
                    break

                print("Error! Enter a positive integer.")

            if reduce_stock(product_id, qty):
                print("Stock successfully reduced!")
            else:
                print("Error! Product not found or insufficient stock.")

        elif choose == "7":
            total = inventory_value()

            print("\n" + "-" * 35)
            print(f"Total Inventory Value: {total:,} UZS")
            print("-" * 35)

        elif choose == "0":
            print("\nThank you for using Inventory System!")
            break

        else:
            print("\nInvalid option! Please choose again.")


if __name__ == "__main__":
    main()
