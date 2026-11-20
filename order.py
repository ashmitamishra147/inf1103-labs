from __future__ import annotations
from discounts import DiscountStrategy, NoDiscount
from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        qty_val = int(quantity)
        if qty_val <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self.product: Product = product
        self.quantity: int = qty_val

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order(self) -> None:
        print(f"--- Order ID: {self.order_id} ---")
        for line in self.order_lines:
            print(
                f"Product: {line.product.name} | Qty: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}"
            )
        print(f"Total Order Value: ${self.calculate_total():.2f}\n")