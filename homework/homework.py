"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from homework.models import Product, Cart


@pytest.fixture
def book():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def pencil():
    return Product("pencil", 10, "This is a book", 2000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_boarder(self, book):
        assert book.check_quantity(999)
        assert book.check_quantity(1000)

    def test_product_check_quantity_negative(self, book):
        assert not book.check_quantity(1001)

    def test_product_buy(self, book):
        book.buy(1000)
        assert book.quantity == 0

    def test_product_buy_more_than_available(self, book):
        with pytest.raises(ValueError):
            book.buy(1001)


class TestCart:
    def test_add_new_product(self, cart, book):
        new_product = 500
        cart.add_product(book, new_product)
        assert cart.products[book] == new_product

    def test_add_additional_product(self, cart, book):
        new_product = 500
        increase_at = 300
        cart.add_product(book, new_product)
        cart.add_product(book, increase_at)
        assert cart.products[book] == new_product + increase_at
        assert len(cart.products.items()) == 1

    def test_remove_product(self, cart, book):
        new_product = 500
        cart.add_product(book, new_product)
        cart.remove_product(book, new_product)
        assert cart.products == {}

    def test_decrease_product(self, cart, book):
        new_product = 200
        decrease_at = 100
        cart.add_product(book, new_product)
        cart.remove_product(book, decrease_at)
        assert cart.products[book] == new_product - decrease_at

    def test_total_price_in_cart(self, cart, book, pencil):
        new_book = 200
        cart.add_product(book, new_book)
        new_pencil = 100
        cart.add_product(pencil, new_pencil)
        total_price = cart.get_total_price()
        assert total_price == new_book * book.price + new_pencil * pencil.price

    def test_clear_cart(self, cart, book, pencil):
        default_amount = 100
        cart.add_product(book, default_amount)
        cart.add_product(pencil, default_amount)
        cart.clear()
        assert cart.products == {}

    def test_not_enough_products_in_stock(self, cart, book):
        with pytest.raises(ValueError):
            cart.add_product(book, 1001)
            cart.buy()

    def test_buy_all(self, book, pencil, cart):
        total_price = cart.get_total_price()
        cart.add_product(book, 500)
        cart.add_product(pencil, 100)
        cart.buy()
        assert cart.products == {}
        assert total_price == 0
