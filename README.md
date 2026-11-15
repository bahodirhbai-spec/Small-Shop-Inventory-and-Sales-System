# Small Shop Inventory and Sales System

A terminal-based Python application designed to help small shop owners manage products, record sales, track stock levels, and view financial reports. Built as a collaborative team project.




## Running

Run the app from any directory:

```bash
python /path/to/Small-Shop-Inventory-and-Sales-System/main.py
```

Product and sales data are always read from and saved next to the code
(`products.json` and `sales.json`), regardless of the current directory.

Product IDs can be entered in full (`P0002`) or by number (`2`). Enter `0`
at an ID or quantity prompt to cancel and return to the menu.

## Key Features

* **Product Management:** Add new products with unique IDs, names, prices in UZS, and initial stock quantities.
* **View & Search:** Display the full inventory list or search for specific items by name or product ID.
* **Stock Replenishment:** Easily restock existing products by adding new units.
* **Sales Recording:** Process customer purchases by selecting a product and quantity, automatically calculating the total and deducting sold units from stock while preventing invalid or out-of-stock sales.




* **Sales History & Reports:**
  * View detailed records of past sales (product, quantity, price at sale, and total).
  * Calculate total sales revenue, average sale amount, and total inventory value using NumPy.
  * Identify the best-selling product by quantity.
  * Receive low-stock alerts for products with 5 or fewer units remaining.
* **Data Persistence:** Automatically saves and reloads all product and sales records using JSON files so no data is lost between sessions.