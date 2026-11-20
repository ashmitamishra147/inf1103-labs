from __future__ import annotations
import csv
from discounts import BulkDiscount, PercentageDiscount
from factory import ProductFactory
from order import Order
from product import Product
from supplier import Supplier


class Inventory:
    def __init__(self):
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product_id: str) -> None:
        self.products = [p for p in self.products if p.product_id != product_id]

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def display_all(self) -> None:
        if not self.products:
            print("Inventory is empty.")
            return
        for product in self.products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}\n")


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip header row
            for row_num, row in enumerate(reader, start=2):
                if not row:
                    continue
                try:
                    if len(row) < 5:
                        raise ValueError("Missing required columns.")
                    product_type = row[0].strip()
                    product_id = row[1].strip()
                    name = row[2].strip()
                    price = float(row[3].strip())
                    stock_quantity = int(row[4].strip())
                    extra = float(row[5].strip()) if len(row) > 5 and row[5].strip() else 0.0

                    product = ProductFactory.create(
                        product_type=product_type,
                        product_id=product_id,
                        name=name,
                        price=price,
                        stock_quantity=stock_quantity,
                        supplier=supplier,
                        extra=extra,
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as exc:
                    print(f"Skipping invalid row {row_num} ({row}): {exc}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def main():
    sup = Supplier("S001", "TechCorp", "support@techcorp.com")
    inventory = Inventory()

    load_products("products.csv", inventory, sup)
    print("\n--- Loaded Inventory ---")
    inventory.display_all()

    if len(inventory.products) >= 2:
        order = Order("ORD-101", discount=BulkDiscount(200, 20))
        order.add_order_line(inventory.products[0], 1)
        order.add_order_line(inventory.products[1], 2)
        order.display_order()

        order.set_discount(PercentageDiscount(10))
        print("After switching to 10% discount:")
        order.display_order()


if __name__ == "__main__":
    main()