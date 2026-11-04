class Product:
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self._name = name
        self._price = float(price)
        self._stock = int(stock)

    @property
    def name(self):
        return self._name

    def display_information(self):
        print(f"ID: {self._product_id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock}")