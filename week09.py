import kiosk

if __name__ == "__main__":
    menu_drinks = ["Ice Americano", "Cafe Latte", "Watermelon Juice"]
    menu_prices = [2000, 3000, 4900]

    menu = kiosk.Menu(menu_drinks, menu_prices)
    order_processor = kiosk.OrderProcessor() # Menu 객체를 생성하지 않음
    order_processor.run(menu) # run 메서드에 Menu 객체를 전달