import os

FILENAME = "inventory.txt"


def load_inventory():
    """Reads saved inventory quantities from inventory.txt.
    
    Returns a list of integer transaction values.
    If file doesn't exist, returns an empty list.
    """
    history = []
    if not os.path.exists(FILENAME):
        return history

    try:
        with open(FILENAME, "r") as file:
            for line in file:
                line = line.strip()
                if line and line.isdigit():
                    history.append(int(line))
    except IOError as e:
        print(f"Error reading {FILENAME}: {e}")

    return history


def save_inventory(history):
    """Writes the full transaction history list to inventory.txt upon exit."""
    try:
        with open(FILENAME, "w") as file:
            for qty in history:
                file.write(f"{qty}\n")
        print(f"Order successfully saved to {FILENAME}")
    except IOError as e:
        print(f"Error saving to {FILENAME}: {e}")


def get_valid_input():
    """Asks user for stock quantity and validates entry.
    
    Returns tuple: (status, value) where status is 'ok', 'quit', or 'invalid'.
    """
    user_input = input("Enter stock quantity (or 'quit' to finish): ")

    if user_input.lower() == "quit":
        return "quit", None

    try:
        quantity = int(user_input)
        if quantity < 0:
            print("Invalid input. Please enter a non-negative stock quantity.")
            return "invalid", None
        return "ok", quantity
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        return "invalid", None


def process_delivery(current_total, new_value):
    """Adds new delivery quantity to current inventory total."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates 10% tax on a delivery."""
    return amount * 0.10


def generate_report(history, total_tax, failed_attempts):
    """Prints the final audit report including transaction history."""
    print("\n--- Inventory Audit Report ---")
    print(f"Transaction History List: {history}")
    print(f"Total Deliveries Processed: {len(history)}")
    print(f"Total Current Inventory:    {sum(history)}")
    print(f"Total Tax Assessed:         ${total_tax:.2f}")
    print(f"Number of Rejected Entries: {failed_attempts}")


def main():
    # 1. Read previously saved inventory at startup [Requirement 1]
    delivery_history = load_inventory()
    
    total_tax = sum(calculate_tax(qty) for qty in delivery_history)
    total_rejected = 0

    if delivery_history:
        print(f"Loaded existing history from {FILENAME}: {delivery_history}")
        print(f"Starting Inventory Total: {sum(delivery_history)}\n")
    else:
        print(f"No existing {FILENAME} found. Starting with empty inventory.\n")

    # 2. Interactive Loop
    while True:
        status, quantity = get_valid_input()

        if status == "quit":
            break

        if status == "invalid":
            total_rejected += 1
            continue

        # Track history in list [Requirement 2]
        delivery_history.append(quantity)
        current_total = sum(delivery_history)
        tax = calculate_tax(quantity)
        total_tax += tax

        print(f"Added {quantity} items to inventory.")
        print(f"Total inventory: {current_total}")
        print(f"Tax for this delivery: ${tax:.2f}\n")

    # 3. Write-back on exit [Requirement 3]
    save_inventory(delivery_history)
    
    # 4. Final Audit Output
    generate_report(delivery_history, total_tax, total_rejected)


if __name__ == "__main__":
    main()