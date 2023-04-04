from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def check_quantity(self, buy_count) -> bool:
        return self.quantity >= buy_count

    def buy(self, buy_count):
        if self.check_quantity(buy_count):
            self.quantity -= buy_count
            return self.quantity
        else:
            raise ValueError('There is not enough products in stock')

    def __hash__(self):
        return hash(self.name + self.description)


@dataclass
class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product not in self.products:
            self.products[product] = buy_count
        else:
            self.products[product] += buy_count

    def remove_product(self, product: Product, buy_count=None):
        """
        Метод удаления продукта из корзины.
        Если quantity не передан, то удаляется вся позиция
        Если quantity больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if buy_count is None or buy_count >= self.products[product]:
            self.products.pop(product)
        else:
            self.products[product] -= buy_count

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        total_price = sum(self.products[product] * product.price for product in self.products)
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        total_price = self.get_total_price()
        for product in self.products:
            product.buy(self.products[product])
        self.clear()
        return total_price


