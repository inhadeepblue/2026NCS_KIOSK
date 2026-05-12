import kiosk as kk
import tkinter as tk

if __name__ == "__main__":
    menu_drinks = ["Ice Americano", "Cafe Latte", "Watermelon Juice", "Ice tea"]
    menu_prices = [2000, 3000, 4900, 3300]

    menu = kk.Menu(menu_drinks, menu_prices)
    order_processor = kk.OrderProcessor(menu)

    root = tk.Tk()
    app = kk.KioskApp(root, menu, order_processor)
    root.mainloop()