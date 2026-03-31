# Refactored Architecture

```mermaid
classDiagram

class OrderManager {
    +create_order(users, inventory, user_id, items)
}

class OrderValidator {
    +validate_user()
    +validate_items()
}

class PriceCalculator {
    +calculate()
}

class DiscountStrategy {
    <<interface>>
    +apply(total)
}

class NoDiscount
class Save10Discount
class Save20Discount

class OrderQuery {
    +save(order)
}

class InventoryService {
    +update()
}

class EmailNotifier {
    +send()
}

OrderManager --> OrderValidator
OrderManager --> PriceCalculator
OrderManager --> OrderQuery
OrderManager --> InventoryService
OrderManager --> EmailNotifier

PriceCalculator --> DiscountStrategy
DiscountStrategy <|-- NoDiscount
DiscountStrategy <|-- Save10Discount
DiscountStrategy <|-- Save20Discount