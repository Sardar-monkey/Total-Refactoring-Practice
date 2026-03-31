from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total):
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total):
        return total

class Save10Discount(DiscountStrategy):
    def apply(self, total):
        return total * 0.9

class Save20Discount(DiscountStrategy):
    def apply(self, total):
        return total * 0.8


class OrderManager:
    def __init__(self, validator, calculator, query, notifier, inventory):
        self.validator = validator
        self.calculator = calculator
        self.query = query
        self.notifier = notifier
        self.inventory = inventory

    def create_order(self, users, inventory, user_id, items):
        self.validator.validate_user(users, user_id)
        self.validator.validate_items(inventory, items)

        total = self.calculator.calculate(inventory, items)

        self.inventory.update(inventory, items)

        order = {
            'id': 1,
            'user': user_id,
            'items': items,
            'total': total,
            'status': 'new'
        }

        self.query.save(order)

        self.notifier.send(
            users[user_id]['email'],
            f'Order {order["id"]} confirmed. Total: {total}'
        )

        return order


class PriceCalculator:
    def __init__(self, tax_rate, discount_strategy):
        self.tax_rate = tax_rate
        self.discount = discount_strategy

    def calculate(self, inventory, items):
        total = 0
        for item_id, qty in items.items():
            total += inventory[item_id]['price'] * qty

        total = self.discount.apply(total)
        total = total * (1 + self.tax_rate)
        return total
    

class OrderValidator:
    def validate_user(self, users, user_id):
        if user_id not in users:
            raise Exception("User not found")
        if users[user_id]['banned']:
            raise Exception("User is banned")

    def validate_items(self, inventory, items):
        for item_id, qty in items.items():
            if item_id not in inventory:
                raise Exception(f'Item {item_id} not found')
            if inventory[item_id]['stock'] < qty:
                raise Exception(f'Insufficient stock for {item_id}')
            

class OrderQuery:
    def __init__(self, db):
        self.db = db
        self.orders = []

    def save(self, order):
        self.orders.append(order)
        self.db.execute(f'INSERT INTO orders VALUES ({order})')


class InventoryService:
    def update(self, inventory, items):
        for item_id, qty in items.items():
            inventory[item_id]['stock'] -= qty


class EmailNotifier:
    def __init__(self, smtp):
        self.smtp = smtp

    def send(self, email, message):
        self.smtp.sendmail('shop@store.com', email, message)