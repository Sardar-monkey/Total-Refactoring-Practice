# States relation diagram

```mermaid
stateDiagram-v2

[*] --> Idle

Idle --> HasMoney : insert_coin
HasMoney --> Dispensing : select_product
Dispensing --> Idle : success
Dispensing --> OutOfStock : stock=0

HasMoney --> Idle : cancel
OutOfStock --> Idle : refill

Idle --> Maintenance
HasMoney --> Maintenance
Maintenance --> Idle
