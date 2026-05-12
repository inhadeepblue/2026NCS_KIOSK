import tkinter as tk
from tkinter import messagebox
import sqlite3

class Menu:
    def __init__(self, drinks, prices):
        if len(drinks) != len(prices):
            raise ValueError("Drinks and prices lists must have the same length.")
        self.drinks = drinks
        self.prices = prices

    def get_price(self, idx):
        if 0 <= idx < len(self.prices):
            return self.prices[idx]
        else:
            raise IndexError("Invalid menu index.")

    def get_drink_name(self, idx):
        if 0 <= idx < len(self.drinks):
            return self.drinks[idx]
        else:
            raise IndexError("Invalid menu index.")

    def get_menu_length(self):
        return len(self.drinks)

class OrderProcessor:
    DISCOUNT_THRESHOLD = 10000
    DISCOUNT_RATE = 0.1

    def __init__(self, menu):
        self.menu = menu
        self.amounts = [0] * menu.get_menu_length()
        self.total_price = 0

        self.conn = sqlite3.connect('queue_number.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            create table if not exists ticket (
            id integer primary key autoincrement,
            number integer not null
            )
        ''')
        self.conn.commit()

    def apply_discount(self, price):
        if price >= self.DISCOUNT_THRESHOLD:
            return price * (1 - self.DISCOUNT_RATE)
        return price

    def process_order(self, idx):
        drink_name = self.menu.get_drink_name(idx)
        drink_price = self.menu.get_price(idx)
        self.total_price += drink_price
        self.amounts[idx] += 1

    def get_receipt(self):
        lines = []
        lines.append(f"{'Product':<15} {'Price':<10} {'Amount':<10} {'Subtotal':<10}")
        lines.append("-" * 50)
        for i in range(self.menu.get_menu_length()):
            if self.amounts[i] > 0:
                drink_name = self.menu.get_drink_name(i)
                drink_price = self.menu.get_price(i)
                lines.append(f"{drink_name:<15} {drink_price:<10} {self.amounts[i]:<10} {drink_price * self.amounts[i]} won")
        discounted_price = self.apply_discount(self.total_price)
        discount = self.total_price - discounted_price
        lines.append("-" * 50)
        lines.append(f"{'Total price before discount:':<30} {self.total_price} won")
        if discount > 0:
            lines.append(f"{'Discount amount:':<30} {int(discount)} won")
            lines.append(f"{'Total price after discount:':<30} {int(discounted_price)} won")
        else:
            lines.append(f"{'No discount applied.':<30}")
            lines.append(f"{'Total price:':<30} {self.total_price} won")
        return "\n".join(lines)

    def get_next_ticket_number(self):
        self.cur.execute('select number from ticket order by number desc limit 1')
        result = self.cur.fetchone()
        if result is None:
            number = 1
            self.cur.execute('insert into ticket (number) values (?)',(number,))
        else:
            number = result[0] + 1
            self.cur.execute('update ticket set number = ? where id = (select id from ticket order by id desc limit 1)', (number,))
        self.conn.commit()
        return number

    def reset(self):
        self.amounts = [0] * self.menu.get_menu_length()
        self.total_price = 0

    def __del__(self):
        self.conn.close()

class KioskApp:
    def __init__(self, root, menu, order_processor):
        self.root = root
        self.menu = menu
        self.order_processor = order_processor

        self.root.title("Cafe Kiosk")
        self.create_widgets()

    def create_widgets(self):
        # 메뉴 버튼
        self.buttons = []
        for idx, (drink, price) in enumerate(zip(self.menu.drinks, self.menu.prices)):
            btn = tk.Button(self.root, text=f"{drink}\n({price}원)", width=16, height=3,
                            command=lambda idx=idx: self.add_order(idx))
            btn.grid(row=0, column=idx, padx=5, pady=5)
            self.buttons.append(btn)

        # 주문내역
        self.order_label = tk.Label(self.root, text="Order List", font=("Arial", 12, "bold"))
        self.order_label.grid(row=1, column=0, columnspan=len(self.menu.drinks), pady=(10,0))

        self.order_text = tk.Text(self.root, width=60, height=10, state='disabled')
        self.order_text.grid(row=2, column=0, columnspan=len(self.menu.drinks), padx=5, pady=5)

        # 결제 및 취소 버튼
        self.finish_button = tk.Button(self.root, text="Finish Order", bg="#4CAF50", fg="white", width=15, command=self.finish_order)
        self.finish_button.grid(row=3, column=0, pady=10)

        self.cancel_button = tk.Button(self.root, text="Cancel All", bg="#F44336", fg="white", width=15, command=self.cancel_order)
        self.cancel_button.grid(row=3, column=1, pady=10)

        self.update_order_text()

    def add_order(self, idx):
        self.order_processor.process_order(idx)
        self.update_order_text()

    def update_order_text(self):
        self.order_text.config(state='normal')
        self.order_text.delete(1.0, tk.END)
        for i in range(self.menu.get_menu_length()):
            if self.order_processor.amounts[i] > 0:
                name = self.menu.get_drink_name(i)
                price = self.menu.get_price(i)
                amount = self.order_processor.amounts[i]
                subtotal = price * amount
                self.order_text.insert(tk.END, f"{name:<15} {price}원 x {amount} = {subtotal}원\n")
        self.order_text.insert(tk.END, f"\nTotal: {self.order_processor.total_price}원")
        if self.order_processor.total_price >= self.order_processor.DISCOUNT_THRESHOLD:
            discounted = int(self.order_processor.apply_discount(self.order_processor.total_price))
            discount = self.order_processor.total_price - discounted
            self.order_text.insert(tk.END, f"\nDiscount: {discount}원\nDiscounted Total: {discounted}원")
        self.order_text.config(state='disabled')

    def finish_order(self):
        if self.order_processor.total_price == 0:
            messagebox.showinfo("Notice", "Please order at least one drink.")
            return
        receipt = self.order_processor.get_receipt()
        ticket = self.order_processor.get_next_ticket_number()
        messagebox.showinfo("Receipt", f"{receipt}\n\nQueue number ticket: {ticket}")
        self.order_processor.reset()
        self.update_order_text()

    def cancel_order(self):
        self.order_processor.reset()
        self.update_order_text()