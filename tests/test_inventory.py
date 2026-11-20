import csv
import pytest
from discounts import BulkDiscount, NoDiscount, PercentageDiscount, StudentDiscount
from factory import ProductFactory
from inventory import Inventory, load_products
from order import Order, OrderLine
from product import DigitalProduct, PhysicalProduct
from supplier import Supplier


@pytest.fixture
def sample_supplier() -> Supplier:
    return Supplier("S001", "TechCorp", "support@techcorp.com")


@pytest.fixture
def sample_physical(sample_supplier: Supplier) -> PhysicalProduct:
    return ProductFactory.create(
        "physical", "P001", "Desk Lamp", 25.00, 10, sample_supplier, 1.5
    )


@pytest.fixture
def sample_digital(sample_supplier: Supplier) -> DigitalProduct:
    return ProductFactory.create(
        "digital", "D001", "Photo Editor", 50.00, 100, sample_supplier, 250.0
    )


def test_factory_creates_physical_and_digital(sample_supplier: Supplier):
    p = ProductFactory.create("physical", "P001", "Lamp", 20.0, 5, sample_supplier, 1.2)
    d = ProductFactory.create("digital", "D001", "App", 15.0, 10, sample_supplier, 50.0)
    assert isinstance(p, PhysicalProduct)
    assert isinstance(d, DigitalProduct)


def test_factory_unknown_type_raises(sample_supplier: Supplier):
    with pytest.raises(ValueError, match="Unknown product type"):
        ProductFactory.create("service", "S001", "Setup", 30.0, 5, sample_supplier)


def test_product_validation_rules(sample_supplier: Supplier):
    with pytest.raises(ValueError):
        ProductFactory.create("physical", "P002", "Bad Price", 0.0, 5, sample_supplier)
    with pytest.raises(ValueError):
        ProductFactory.create("physical", "P003", "Bad Price", -10.0, 5, sample_supplier)
    with pytest.raises(ValueError):
        ProductFactory.create("digital", "D002", "Bad Stock", 10.0, -1, sample_supplier)


def test_order_line_quantity_validation(sample_physical: PhysicalProduct):
    with pytest.raises(ValueError):
        OrderLine(sample_physical, 0)
    with pytest.raises(ValueError):
        OrderLine(sample_physical, -2)


def test_order_discount_strategies_and_switching(
    sample_physical: PhysicalProduct, sample_digital: DigitalProduct
):
    order = Order("ORD-1", discount=NoDiscount())
    order.add_order_line(sample_physical, 2)  # 50.0
    order.add_order_line(sample_digital, 4)   # 200.0 -> total 250.0
    assert order.calculate_total() == pytest.approx(250.0)

    order.set_discount(BulkDiscount(200, 20))
    assert order.calculate_total() == pytest.approx(230.0)

    order.set_discount(PercentageDiscount(10))
    assert order.calculate_total() == pytest.approx(225.0)

    order.set_discount(StudentDiscount(5))
    assert order.calculate_total() == pytest.approx(237.5)


def test_load_products_skips_bad_rows_and_handles_missing_file(
    tmp_path, sample_supplier: Supplier
):
    inv = Inventory()
    missing_file = tmp_path / "does_not_exist.csv"
    load_products(str(missing_file), inv, sample_supplier)
    assert len(inv.products) == 0

    csv_file = tmp_path / "products.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_type", "product_id", "name", "price", "stock_quantity"])
        writer.writerow(["physical", "P001", "Desk Lamp", "25.00", "10"])
        writer.writerow(["service", "S001", "Installation", "30.00", "5"])
        writer.writerow(["physical", "P002", "Office Chair", "abc", "3"])
        writer.writerow(["digital", "D001", "Photo Editor", "49.90", "100"])

    load_products(str(csv_file), inv, sample_supplier)
    assert len(inv.products) == 2