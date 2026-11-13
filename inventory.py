from __future__ import annotations
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier
from order import Order

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

def main():
    sup = Supplier("S001", "TechCorp", "support@techcorp.com")
    
    p1 = PhysicalProduct("P101", "Laptop", 1200.0, 10, sup, 2.5)
    d1 = DigitalProduct("D201", "Antivirus Sub", 49.99, 100, sup, 15.0)

    inventory = Inventory()
    inventory.add_product(p1)
    inventory.add_product(d1)

    print("--- Inventory Display (Polymorphism) ---")
    inventory.display_all()

    order = Order("ORD-001")
    order.add_order_line(p1, 1)
    order.add_order_line(d1, 2)
    order.display_order()

if __name__ == "__main__":
    main()