from product import Product

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def display_all(self):
        if not self.products:
            print("Inventory is empty.")
        for product in self.products:
            product.display_information()

    def search_product(self, search_name):
        found = False
        for product in self.products:
            if search_name.lower() in product.name.lower():
                product.display_information()
                found = True
        if not found:
            print("Product not found.")

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
            p_id = input("Enter Product ID: ")
            name = input("Enter Name: ")
            price = float(input("Enter Price: "))
            stock = int(input("Enter Stock: "))

            new_product = Product(p_id, name, price, stock)
            inventory.add_product(new_product)
            print("Product added successfully!")

        elif choice == '3':
            pass

        elif choice == '4':
            search_name = input("Enter product name to search: ")
            inventory.search_product(search_name)

        elif choice == '5':
            print("Inventory saved!")

        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()