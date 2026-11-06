def get_valid_input():
    user_input = input("Enter stock quantity or 'quit' to exit: ")

    if user_input.lower() == "quit":
        return "quit"

    try:
        quantity = int(user_input)

        if quantity < 0:
            return None

        return quantity

    except ValueError:
        return None


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_deliveries, failed_attempts):
    print(f"Total Deliveries Processed: {total_deliveries}")
    print(f"Total rejected entries: {failed_attempts}")


total_inventory = 0
total_rejected = 0
total_deliveries = 0

while True:
    quantity = get_valid_input()

    if quantity == "quit":
        break

    if quantity is None:
        print("Invalid input. Please enter a non-negative stock quantity.")
        total_rejected += 1
        continue

    if total_inventory + quantity > 500:
        print(
            f"Overstock alert! You cannot add {quantity} items. "
            "Maximum capacity is 500."
        )
        total_rejected += 1
        continue

    total_inventory = process_delivery(total_inventory, quantity)

    tax = calculate_tax(quantity)

    total_deliveries += 1

    print(
        f"Added {quantity} items to inventory. "
        f"Total inventory: {total_inventory}"
    )
    print(f"Tax for this delivery: {tax}")


generate_report(total_deliveries, total_rejected)