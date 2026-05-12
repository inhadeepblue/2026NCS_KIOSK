import tkinter as tk
from kiosk import KioskGUI

if __name__ == "__main__":
    menu_drinks = ["Ice Americano", "Cafe Latte", "Watermelon Juice", "Ice tea", "Espresso"]
    menu_prices = [2000, 3000, 4900, 3300, 2500]

    root = tk.Tk()
    app = KioskGUI(root, menu_drinks, menu_prices)
    root.mainloop()