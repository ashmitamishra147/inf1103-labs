from product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

class Order:
    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = 0.0
        for line in self.order_lines:
            total += line.calculate_subtotal()
        return total

    def display_order(self) -> None:
        print(f"--- Order ID: {self.order_id} ---")
        for line in self.order_lines:
            print(f"Product: {line.product.name} | Qty: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
        print(f"Total Order Value: ${self.calculate_total():.2f}\n")