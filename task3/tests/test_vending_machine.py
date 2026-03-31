import sys
sys.path.insert(0, '.') 

import pytest
from refactored.VendingMachine import VendingMachine
from refactored import States

@pytest.fixture
def machine():
    products = {
        1: {"name": "Soda", "price": 2, "stock": 1},
        2: {"name": "Chips", "price": 1, "stock": 0},
    }
    return VendingMachine(products)

def test_insert_coin_changes_state(machine):
    assert isinstance(machine.state, States.IdleState)
    machine.insert_coin(2)
    assert machine.balance == 2
    assert isinstance(machine.state, States.HasMoneyState)

def test_select_product_without_money(machine, capsys):
    machine.select_product(1)
    captured = capsys.readouterr()
    assert "Insert money first" in captured.out

def test_buy_product_success(machine, capsys):
    machine.insert_coin(2)
    machine.select_product(1)
    captured = capsys.readouterr()
    assert "Dispensing Soda" in captured.out
    assert machine.balance == 0
    assert machine.products[1]["stock"] == 0
    assert isinstance(machine.state, States.OutOfStockState)

def test_buy_product_insufficient_money(machine, capsys):
    machine.insert_coin(1)
    machine.select_product(1)
    captured = capsys.readouterr()
    assert "Not enough money" in captured.out
    assert machine.balance == 1
    assert isinstance(machine.state, States.HasMoneyState)

def test_cancel_returns_money(machine, capsys):
    machine.insert_coin(2)
    machine.cancel()
    captured = capsys.readouterr()
    assert "Returning 2" in captured.out
    assert machine.balance == 0
    assert isinstance(machine.state, States.IdleState)

def test_refill_out_of_stock(machine):
    assert machine.products[2]["stock"] == 0
    machine.refill(2, 3)
    assert machine.products[2]["stock"] == 3