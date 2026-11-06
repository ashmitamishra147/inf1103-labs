from product import PhysicalProduct, DigitalProduct
import json
import os

class Inventory:
    def __init__(self, filepath="inventory.json"):
        self.products = []
        self.filepath = filepath
        self.load_from_json()

    def add_product(self, product):
        self.products.append(product)
        self.save_to_json()

    def display_all(self):
        if not self.products:
            print("\nInventory is empty.")
            return
        print("\n--- Inventory Products ---")
        for product in self.products:
            product.display_information()
            print(f"  -> Fulfilment: {product.get_fulfilment_info()}")
            if isinstance(product, PhysicalProduct):
                print(f"  -> Shipping Cost: ${product.calculate_shipping_cost():.2f}")
            print("-" * 50)

    def search_product(self, search_name):
        found = False
        print(f"\n--- Search Results for '{search_name}' ---")
        for product in self.products:
            if search_name.lower() in product.name.lower():
                product.display_information()
                print(f"  -> Fulfilment: {product.get_fulfilment_info()}")
                if isinstance(product, PhysicalProduct):
                    print(f"  -> Shipping Cost: ${product.calculate_shipping_cost():.2f}")
                print("-" * 50)
                found = True
        if not found:
            print("Product not found.")

    def update_stock(self, product_id, quantity):
        for product in self.products:
            if product.product_id == product_id:
                product.update_stock(quantity)
                self.save_to_json()
                print("Stock updated successfully!")
                return True
        print("Product ID not found.")
        return False

    def save_to_json(self):
        data = []
        for p in self.products:
            if isinstance(p, PhysicalProduct):
                item = {
                    "type": "physical",
                    "product_id": p.product_id,
                    "name": p.name,
                    "price": p.price,
                    "stock": p.stock,
                    "weight": p.weight
                }
            elif isinstance(p, DigitalProduct):
                item = {
                    "type": "digital",
                    "product_id": p.product_id,
                    "name": p.name,
                    "price": p.price,
                    "stock": p.stock,
                    "download_size": p.download_size
                }
            data.append(item)
        try:
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving inventory: {e}")

    def load_from_json(self):
        if not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                self.products = []
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
                    self.products.append(product)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading inventory: {e}")


def main():
    inventory = Inventory()

    while True:
        print("\n--- Inventory Menu ---")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ")

        if choice == '1':
            inventory.display_all()

        elif choice == '2':
            print("\nSelect Product Type:")
            print("1. Physical Product")
            print("2. Digital Product")
            p_type = input("Enter choice (1-2): ")

            p_id = input("Enter Product ID: ")
            name = input("Enter Name: ")
            price = float(input("Enter Price: "))
            stock = int(input("Enter Stock: "))

            if p_type == '1':
                weight = float(input("Enter Weight (kg): "))
                new_product = PhysicalProduct(p_id, name, price, stock, weight)
            elif p_type == '2':
                download_size = float(input("Enter Download Size (MB): "))
                new_product = DigitalProduct(p_id, name, price, stock, download_size)
            else:
                print("Invalid product type. Product creation cancelled.")
                continue

            inventory.add_product(new_product)
            print("Product added and saved successfully!")

        elif choice == '3':
            p_id = input("Enter Product ID to update stock: ")
            try:
                qty = int(input("Enter quantity to add (use negative to reduce): "))
                inventory.update_stock(p_id, qty)
            except ValueError:
                print("Invalid quantity. Please enter an integer.")

        elif choice == '4':
            search_name = input("Enter product name to search: ")
            inventory.search_product(search_name)

        elif choice == '5':
            inventory.save_to_json()
            print("Inventory saved successfully!")

        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()