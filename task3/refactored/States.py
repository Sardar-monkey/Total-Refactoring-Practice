from abc import ABC

class State(ABC):

    def insert_coin(self, machine, amount):
        pass

    def select_product(self, machine, product_id):
        pass

    def cancel(self, machine):
        pass

    def refill(self, machine, product_id, qty):
        pass


class IdleState(State):

    def insert_coin(self, machine, amount):
        machine.balance += amount
        print(f"Accepted {amount}")
        machine.set_state(HasMoneyState())

    def select_product(self, machine, product_id):
        print("Insert money first")

    def cancel(self, machine):
        print("Nothing to cancel")

    def refill(self, machine, product_id, qty):
        machine.products[product_id]['stock'] += qty


class HasMoneyState(State):

    def insert_coin(self, machine, amount):
        machine.balance += amount
        print(f"Balance: {machine.balance}")

    def select_product(self, machine, product_id):
        product = machine.products.get(product_id)

        if not product:
            print("Invalid product")
            return

        if product['stock'] == 0:
            machine.set_state(OutOfStockState())
            return

        if machine.balance < product['price']:
            print("Not enough money")
            return

        machine.set_state(DispensingState())
        machine.state.dispense(machine, product)

    def cancel(self, machine):
        print(f"Returning {machine.balance}")
        machine.balance = 0
        machine.set_state(IdleState())

    def refill(self, machine, product_id, qty):
        machine.products[product_id]['stock'] += qty


class DispensingState(State):

    def dispense(self, machine, product):
        machine.balance -= product['price']
        product['stock'] -= 1

        print(f"Dispensing {product['name']}")

        if product['stock'] == 0:
            machine.set_state(OutOfStockState())
        else:
            machine.set_state(IdleState())

    def insert_coin(self, machine, amount):
        print("Wait...")

    def select_product(self, machine, product_id):
        print("Wait...")

    def cancel(self, machine):
        print("Already dispensing")

    def refill(self, machine, product_id, qty):
        pass


class OutOfStockState(State):

    def insert_coin(self, machine, amount):
        print("Out of stock")

    def select_product(self, machine, product_id):
        print("Out of stock")

    def cancel(self, machine):
        print(f"Returning {machine.balance}")
        machine.balance = 0
        machine.set_state(IdleState())

    def refill(self, machine, product_id, qty):
        machine.products[product_id]['stock'] += qty
        machine.set_state(IdleState())


class MaintenanceState(State):

    def insert_coin(self, machine, amount):
        print("Maintenance mode")

    def select_product(self, machine, product_id):
        print("Maintenance mode")

    def cancel(self, machine):
        print("Maintenance mode")

    def refill(self, machine, product_id, qty):
        machine.products[product_id]['stock'] += qty
        print("Refilled in maintenance")