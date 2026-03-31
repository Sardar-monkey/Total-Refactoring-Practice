import unittest
from unittest.mock import Mock
from src.OrderManagerBetter import OrderManager

class TestOrderManager(unittest.TestCase):

    def test_create_order(self):
        validator = Mock()
        calculator = Mock()
        repo = Mock()
        notifier = Mock()
        inventory = Mock()

        manager = OrderManager(
            validator,
            calculator,
            repo,
            notifier,
            inventory
        )

        users = {1: {'email': 'test@mail.com', 'banned': False}}
        items = {'item1': 1}
        inv = {'item1': {'price': 100, 'stock': 10}}

        order = manager.create_order(users, inv, 1, items)

        validator.validate_user.assert_called()
        repo.save.assert_called()
        notifier.send.assert_called()