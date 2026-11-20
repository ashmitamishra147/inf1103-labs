from inventory import Inventory
from models import PhysicalProduct, DigitalProduct

def main():
    inventory = Inventory()

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Display All Products")
        print("2. Add Physical Product")
        print("3. Add Digital Product")
        print("4. Update Stock Quantity")
        print("5. Search for a Product")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            products = inventory.display_all()
            if not products:
                print("\nInventory is currently empty.")
            else:
                print("\n--- Current Inventory ---")
                for info in products:
                    print(info)
                    
        elif choice in ('2', '3'):
            is_physical = (choice == '2')
            p_type_str = "Physical" if is_physical else "Digital"
            print(f"\n--- Add New {p_type_str} Product ---")
            
            p_id = input("Enter Product ID: ").strip()
            name = input("Enter Product Name: ").strip()
            
            try:
                price = float(input("Enter Price ($): "))
                stock = int(input("Enter Initial Stock Quantity: "))
                
                if is_physical:
                    weight = float(input("Enter Weight (kg): "))
                    product = PhysicalProduct(p_id, name, price, stock, weight)
                else:
                    download_size = float(input("Enter Download Size (MB): "))
                    product = DigitalProduct(p_id, name, price, stock, download_size)
                
                if inventory.add_product(product):
                    print(f"\nSuccess: {name} added to inventory!")
                    print(f"Fulfilment Info: {product.get_fulfilment_info()}")
                    if isinstance(product, PhysicalProduct):
                        print(f"Estimated Shipping Cost: ${product.calculate_shipping_cost():.2f}")
                else:
                    print(f"\nError: Product ID '{p_id}' already exists.")
            except ValueError:
                print("\nInvalid input format. Please enter appropriate numeric values for price, stock, and size/weight.")
                
        elif choice == '4':
            print("\n--- Update Stock ---")
            p_id = input("Enter Product ID: ").strip()
            try:
                qty_change = int(input("Enter stock change amount (use positive to add, negative to reduce): "))
                if inventory.update_stock(p_id, qty_change):
                    print("\nStock updated successfully.")
                else:
                    print(f"\nProduct ID '{p_id}' not found.")
            except ValueError:
                print("\nInvalid quantity format.")
                
        elif choice == '5':
            print("\n--- Search Product ---")
            p_id = input("Enter Product ID to search: ").strip()
            product = inventory.find_product(p_id)
            if product:
                print(f"\nFound:\n{product.display_information()}")
                print(f"Fulfilment: {product.get_fulfilment_info()}")
                if hasattr(product, 'calculate_shipping_cost'):
                    print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
            else:
                print(f"\nProduct ID '{p_id}' not found.")
                
        elif choice == '6':
            print("\nExiting Inventory Management System. Data saved securely.")
            break
        else:
            print("\nInvalid selection. Please choose a number between 1 and 6.")

if __name__ == "__main__":
    main()