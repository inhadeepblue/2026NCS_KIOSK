```mermaid
classDiagram
    class Menu {
        +List~str~ drinks
        +List~int~ prices
        +__init__(drinks: List~str~, prices: List~int~)
        +display_menu() str
        +get_price(idx: int) int
        +get_drink_name(idx: int) str
        +get_menu_length() int
    }

    class OrderProcessor {
        +int DISCOUNT_THRESHOLD
        +float DISCOUNT_RATE
        +Menu menu
        +List~int~ amounts
        +int total_price
        +__init__(menu: Menu)
        +apply_discount(price: int) float
        +process_order(idx: int) None
        +print_receipt() None
        +run() None
    }

    %% Aggregation (Has-a) 관계: OrderProcessor가 Menu를 소유함
    OrderProcessor "1" o-- "1" Menu : aggregation
```