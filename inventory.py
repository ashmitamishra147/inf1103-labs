import json
import os
from models import PhysicalProduct, DigitalProduct

class Inventory:
    """Manages the collection of products and JSON persistence."""
    
    def __init__(self, filepath: str = "inventory_data.json"):
        self._products = {}
        self._filepath = filepath
        self.load_from_file()

    def add_product(self, product) -> bool:
        if product.product_id in self._products:
            return False
        self._products[product.product_id] = product
        self.save_to_file()
        return True

    def find_product(self, product_id: str):
        return self._products.get(product_id)

    def update_stock(self, product_id: str, quantity: int) -> bool:
        product = self.find_product(product_id)
        if product:
            product.update_stock(quantity)
            self.save_to_file()
            return True
        return False

    def display_all(self) -> list:
        return [p.display_information() for p in self._products.values()]

    def save_to_file(self) -> None:
        data = [p.to_dict() for p in self._products.values()]
        try:
            with open(self._filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving inventory to file: {e}")

    def load_from_file(self) -> None:
        if not os.path.exists(self._filepath):
            return
        
        try:
            with open(self._filepath, 'r') as f:
                data = json.load(f)
                self._products.clear()
                for item in data:
                    ptype = item.get("type")
                    if ptype == "physical":
                        product = PhysicalProduct(
                            item["product_id"], item["name"], item["price"], item["stock"], item["weight"]
                        )
                    elif ptype == "digital":
                        product = DigitalProduct(
                            item["product_id"], item["name"], item["price"], item["stock"], item["download_size"]
                        )
                    else:
                        continue
                    self._products[product.product_id] = product
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading inventory from file: {e}")