from __future__ import annotations
from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier):
        self.product_id: str = product_id
        self._name: str = name
        self.price: float = float(price)
        self.stock_quantity: int = int(stock_quantity)
        self.supplier: Supplier = supplier

    @property
    def name(self) -> str:
        return self._name

    def display_information(self) -> None:
        print(f"ID: {self.product_id} | Name: {self._name} | Price: ${self.price:.2f} | Stock: {self.stock_quantity}")
        if self.supplier:
            print("  -> Supplier Info:", end=" ")
            self.supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

class PhysicalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, weight_kg: float):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.weight_kg: float = float(weight_kg)

    def get_fulfilment_info(self) -> str:
        return f"Physical shipping weight: {self.weight_kg} kg"

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, file_size_mb: float):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.file_size_mb: float = float(file_size_mb)

    def get_fulfilment_info(self) -> str:
        return f"Digital download size: {self.file_size_mb} MB"