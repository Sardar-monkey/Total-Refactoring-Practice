from . import States
class VendingMachine:

    def __init__(self, products):
        self.products = products
        self.balance = 0
        self.state = States.IdleState()

    def set_state(self, state):
        self.state = state

    def insert_coin(self, amount):
        self.state.insert_coin(self, amount)

    def select_product(self, product_id):
        self.state.select_product(self, product_id)

    def cancel(self):
        self.state.cancel(self)

    def refill(self, product_id, qty):
        self.state.refill(self, product_id, qty)