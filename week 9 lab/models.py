from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    """Interface-style abstract base class for items that can be physically shipped."""
    
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculate and return the shipping cost."""
        pass


class Product(ABC):
    """Abstract base class representing a generic product in the inventory."""
    
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def update_stock(self, quantity: int) -> None:
        """Update the stock quantity."""
        self._stock += quantity
        if self._stock < 0:
            self._stock = 0

    def display_information(self) -> str:
        """Return common product information string."""
        return f"ID: {self._product_id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock}"

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method defining how the product is fulfilled."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize product attributes into a dictionary for JSON storage."""
        pass


class PhysicalProduct(Product, CanBeShipped):
    """Subclass representing a physical product that requires shipping and has weight."""
    
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> str:
        base_info = super().display_information()
        return f"{base_info} | Type: Physical | Weight: {self._weight}kg"

    def get_fulfilment_info(self) -> str:
        return "This physical product requires packing and physical shipping."

    def calculate_shipping_cost(self) -> float:
        # Simple rule: Base fee $5.00 + $2.50 per kg
        return 5.00 + (self._weight * 2.50)

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "weight": self._weight
        }


class DigitalProduct(Product):
    """Subclass representing a digital product delivered online with a download size."""
    
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> str:
        base_info = super().display_information()
        return f"{base_info} | Type: Digital | Download Size: {self._download_size}MB"

    def get_fulfilment_info(self) -> str:
        return "This digital product is delivered instantly via a secure download link."

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "download_size": self._download_size
        }