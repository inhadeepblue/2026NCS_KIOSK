import tkinter as tk
from kiosk import KioskGUI
import requests


if __name__ == "__main__":
    url = f"https://wttr.in/incheon?&0&Q"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text.strip())
    else:
        print(f"상태 코드 : {response.status_code}")

    menu_drinks = ["Ice Americano", "Cafe Latte", "Watermelon Juice", "Ice tea"]
    menu_prices = [2000, 3000, 4900, 3500]

    root = tk.Tk()
    app = KioskGUI(root, menu_drinks, menu_prices)
    root.mainloop()