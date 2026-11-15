# Small Shop Inventory and Sales System

A terminal-based Python application designed to help small shop owners manage products,
record sales, track stock levels, and view financial reports. Built as a collaborative
team project.

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

* **Product Management:** Add new products with unique IDs, names, prices in UZS, and
  initial stock quantities.
* **View & Search:** Display the full inventory list or search for specific items by
  name or product ID.
* **Stock Replenishment:** Easily restock existing products by adding new units.
* **Sales Recording:** Process customer purchases by selecting a product and quantity,
  automatically calculating the total and deducting sold units from stock while
  preventing invalid or out-of-stock sales.
* **Sales History & Reports:**
  * View detailed records of past sales (product, quantity, price at sale, and total).
  * Calculate total sales revenue, average sale amount, and total inventory value using
    NumPy.
  * Identify the best-selling product by quantity.
  * Receive low-stock alerts for products with 5 or fewer units remaining.
* **Data Persistence:** Automatically saves and reloads all product and sales records
  using JSON files so no data is lost between sessions.

## Project Structure

```text
.
├── main.py           # Entry point and interactive menu
├── inventory.py      # Products, stock, search, restock and inventory value
├── sales.py          # Sales recording, sales history and reports
├── storage.py        # Compatibility layer re-exporting product storage helpers
├── products.json     # Saved product data
├── sales.json        # Saved sales data
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## Requirements

* Python 3.10 or newer (tested with Python 3.14)
* `pip` and `venv` (usually included with Python)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/bahodirhbai-spec/Small-Shop-Inventory-and-Sales-System.git
cd Small-Shop-Inventory-and-Sales-System
```

### 2. Create and activate a virtual environment

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

The program can also be started from another directory:

```bash
python /path/to/Small-Shop-Inventory-and-Sales-System/main.py
```

`products.json` and `sales.json` are always read from and written next to the code,
regardless of the current working directory.

## Usage Notes

* Product IDs can be entered in full (`P0002`) or by number (`2`).
* Enter `0` at an ID or quantity prompt to cancel the current action and return to the
  menu.
* Prices are entered in UZS and must be positive whole numbers.
* Stock quantities must be whole numbers; stock may be zero.

## Team Contributions

* **Bahodirjon** — Repository setup and maintenance; core inventory module (add, list,
  search, restock, reduce stock, inventory value); sales recording and persistence;
  NumPy-based reports; Pydantic data validation; application menu in `main.py`;
  `.gitignore` and project documentation.
* **Hasan** — Product ID normalization so IDs can be entered as `P0002` or `2`;
  unified data-storage layer with paths resolved relative to the source files;
  improved input validation, cancel handling and error handling across the menu and
  sales workflow; README notes for running the application.

## License

This project was created for educational purposes as part of a collaborative team
assignment.
