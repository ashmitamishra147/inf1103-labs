total_inventory = 0
total_rejected = 0

while True:
    user_input = input("Enter stock quantity or 'quit' to exit: ")
    
    if user_input.lower() == 'quit':
        break
        
    try:
        val = float(user_input)
        quantity = int(val)
        
        if quantity < 0:
            print("Invalid input. Please enter a non-negative stock quantity.")
            total_rejected += 1
        elif total_inventory + quantity > 500:
            print(f"Overstock alert! You cannot add {quantity} items. Maximum capacity is 500.")
            total_rejected += 1
        else:
            total_inventory += quantity
            print(f"Added {quantity} items to inventory. Total inventory: {total_inventory}")
            
    except ValueError:
        print("Invalid input. Please enter a valid stock quantity or 'quit' to exit.")
        total_rejected += 1

print(f"Total Units Processed: {total_inventory}")
print(f"Total rejected entries: {total_rejected}")
