import kiosk

if __name__ == "__main__":
    menu_drinks = ["Ice Americano", "Cafe Latte", "Watermelon Juice", "Espresso"]
    menu_prices = [2000, 3000, 4900, 2500]

    menu = kiosk.Menu(menu_drinks, menu_prices)
    order_processor = kiosk.OrderProcessor(menu)
    order_processor.run()