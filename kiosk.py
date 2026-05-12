import tkinter as tk
from tkinter import messagebox
import sqlite3
from typing import List


class Menu:
    """Represents the cafe menu."""

    def __init__(self, drinks: List[str], prices: List[int]):
        """
        Initialization method for the Menu class.
        :param drinks: beverage name list
        :param prices: beverage price list
        """
        if len(drinks) != len(prices):
            raise ValueError("Drinks and prices lists must have the same length.")

        self.drinks = drinks
        self.prices = prices

    def display_menu(self) -> str:
        """
        Generate a dynamic menu string
        :return: formatted menu string
        """
        return "".join(
            [f"{k + 1}) {self.drinks[k]} {self.prices[k]} won\n"
             for k in range(len(self.drinks))]
        ) + f"{len(self.drinks) + 1}) Exit : "

    def get_price(self, idx: int) -> int:
        """
        Get the price of a drink at a given index.
        :param idx: index of the drink
        :return: price of the drink
        """
        if 0 <= idx < len(self.prices):
            return self.prices[idx]
        else:
            raise IndexError("Invalid menu index.")

    def get_drink_name(self, idx: int) -> str:
        """
        Get the name of a drink at a given index.
        :param idx: index of the drink
        :return: name of the drink
        """
        if 0 <= idx < len(self.drinks):
            return self.drinks[idx]
        else:
            raise IndexError("Invalid menu index.")

    def get_menu_length(self) -> int:
        """
        Get the number of items on the menu.
        :return: the length of the menu
        """
        return len(self.drinks)


class OrderProcessor:
    """Processes cafe orders, applies discounts, and prints receipts."""
    DISCOUNT_THRESHOLD = 10000
    DISCOUNT_RATE = 0.1

    def __init__(self, menu: Menu) -> None:
        """
        Initialization method for the OrderProcessor class.
        :param menu: An instance of the Menu class.
        :return: None
        """
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

    def apply_discount(self, price: int) -> float:
        """
        Apply discount rate when the total amount exceeds a certain threshold
        :param price: price before discount
        :return: price after discount
        """
        if price >= self.DISCOUNT_THRESHOLD:
            return price * (1 - self.DISCOUNT_RATE)
        return price

    def process_order(self, idx: int) -> None:
        """
        Process the order and accumulate the total price
        :param idx: index of the ordered drink
        :return: None
        """
        drink_name = self.menu.get_drink_name(idx)
        drink_price = self.menu.get_price(idx)

        print(f"{drink_name} ordered. Price: {drink_price} won")
        self.total_price += drink_price
        self.amounts[idx] += 1

    def get_receipt_text(self) -> str:
        """
        Return order summary and final price with formatted alignment
        :return: formatted receipt text as string
        """
        receipt_text = f"{'Product':<15} {'Price':<10} {'Amount':<10} {'Subtotal':<10}\n"
        receipt_text += "-" * 50 + "\n"

        for i in range(self.menu.get_menu_length()):
            if self.amounts[i] > 0:
                drink_name = self.menu.get_drink_name(i)
                drink_price = self.menu.get_price(i)

                receipt_text += f"{drink_name:<15} {drink_price:<10} {self.amounts[i]:<10} {drink_price * self.amounts[i]} won\n"

        discounted_price = self.apply_discount(self.total_price)
        discount = self.total_price - discounted_price

        receipt_text += "-" * 50 + "\n"
        receipt_text += f"{'Total price before discount:':<30} {self.total_price} won\n"
        if discount > 0:
            receipt_text += f"{'Discount amount:':<30} {discount} won\n"
            receipt_text += f"{'Total price after discount:':<30} {discounted_price} won\n"
        else:
            receipt_text += f"{'No discount applied.':<30}\n"
            receipt_text += f"{'Total price:':<30} {self.total_price:>5} won\n"

        return receipt_text

    def get_next_ticket_number(self) -> int:
        """
        Function that Produce next ticket number (Database version)
        :return: next ticket number
        """
        self.cur.execute('select number from ticket order by number desc limit 1')
        result = self.cur.fetchone()

        if result is None:
            number = 1
            self.cur.execute('insert into ticket (number) values (?)', (number,))
        else:
            number = result[0] + 1
            # self.cur.execute('insert into ticket (number) values (?)', (number,))
            self.cur.execute('update ticket set number = ? where id = (select id from ticket order by id desc limit 1)',
                             (number,))

        self.conn.commit()
        return number

    def __del__(self) -> None:
        """
        Destructor method for OrderProcessor - close database connection
        :return: None
        """
        print('End program')
        self.conn.close()  # db connection close ....


class KioskGUI:
    def __init__(self, root: tk.Tk, menu_drinks: List[str], menu_prices: List[int]) -> None:
        self.root = root
        self.root.title("Cafe Kiosk")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Initialize menu and order processor
        self.menu = Menu(menu_drinks, menu_prices)
        self.order_processor = OrderProcessor(self.menu)

        # Create UI components
        self.create_widgets()

    def create_widgets(self) -> None:
        """Create and initialize all GUI widgets"""
        # Title frame
        title_frame = tk.Frame(self.root, bg="#4a7abc", padx=10, pady=10)
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

        title_label = tk.Label(title_frame, text="Cafe Kiosk", font=("Arial", 24, "bold"), bg="#4a7abc", fg="white")
        title_label.grid(row=0, column=0)

        # Menu buttons frame
        menu_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        menu_frame.grid(row=1, column=0, sticky="nsew")

        menu_label = tk.Label(menu_frame, text="Menu", font=("Arial", 18, "bold"), bg="#f0f0f0")
        menu_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Create menu buttons
        for i in range(self.menu.get_menu_length()):
            drink_name = self.menu.get_drink_name(i)
            drink_price = self.menu.get_price(i)

            # Button with drink name and price
            btn = tk.Button(
                menu_frame,
                text=f"{drink_name}\n{drink_price} won",
                font=("Arial", 12),
                width=15,
                height=3,
                bg="#e0e0e0",
                command=lambda idx=i: self.add_to_order(idx)
            )
            btn.grid(row=(i // 2) + 1, column=i % 2, padx=5, pady=5, sticky="nsew")

        # Order summary frame
        order_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        order_frame.grid(row=1, column=1, sticky="nsew")

        order_label = tk.Label(order_frame, text="Current Order", font=("Arial", 18, "bold"), bg="#f0f0f0")
        order_label.grid(row=0, column=0, pady=(0, 10))

        # Text widget to display current order
        self.order_text = tk.Text(order_frame, width=40, height=15, font=("Courier", 10))
        self.order_text.grid(row=1, column=0, padx=5, pady=5)
        self.order_text.config(state=tk.DISABLED)

        # Control buttons frame
        control_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        control_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Complete order button
        complete_btn = tk.Button(
            control_frame,
            text="Complete Order",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=self.complete_order
        )
        complete_btn.grid(row=0, column=0, padx=5, pady=5)

        # Reset order button
        reset_btn = tk.Button(
            control_frame,
            text="Reset Order",
            font=("Arial", 12, "bold"),
            bg="#f44336",
            fg="white",
            padx=10,
            pady=5,
            command=self.reset_order
        )
        reset_btn.grid(row=0, column=1, padx=5, pady=5)

        # Exit button
        exit_btn = tk.Button(
            control_frame,
            text="Exit",
            font=("Arial", 12, "bold"),
            bg="#607D8B",
            fg="white",
            padx=10,
            pady=5,
            command=self.exit_program
        )
        exit_btn.grid(row=0, column=2, padx=5, pady=5)

        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def add_to_order(self, idx: int) -> None:
        """
        Add the selected drink to the order
        :param idx: index of the drink in the menu
        """
        self.order_processor.process_order(idx)
        self.update_order_display()

    def update_order_display(self) -> None:
        """Update the order summary in the text widget"""
        # Enable text widget for editing
        self.order_text.config(state=tk.NORMAL)
        # Clear current content
        self.order_text.delete(1.0, tk.END)

        # Add current order information
        order_info = "Current Order:\n\n"

        for i in range(self.menu.get_menu_length()):
            if self.order_processor.amounts[i] > 0:
                drink_name = self.menu.get_drink_name(i)
                drink_price = self.menu.get_price(i)
                subtotal = drink_price * self.order_processor.amounts[i]

                order_info += f"{drink_name}: {self.order_processor.amounts[i]} × {drink_price} = {subtotal} won\n"

        # Check if discount should be applied and show in the display
        total_price = self.order_processor.total_price
        if total_price >= self.order_processor.DISCOUNT_THRESHOLD:
            discounted_price = self.order_processor.apply_discount(total_price)
            discount_amount = total_price - discounted_price

            order_info += f"\nTotal before discount: {total_price} won"
            order_info += f"\nDiscount ({int(self.order_processor.DISCOUNT_RATE * 100)}%): {discount_amount} won"
            order_info += f"\nTotal after discount: {discounted_price} won"
        else:
            order_info += f"\nTotal: {total_price} won"
            # Show how much more to spend for discount
            if total_price > 0:
                remaining = self.order_processor.DISCOUNT_THRESHOLD - total_price
                order_info += f"\n(Spend {remaining} won more for {int(self.order_processor.DISCOUNT_RATE * 100)}% discount)"

        self.order_text.insert(tk.END, order_info)
        # Disable editing
        self.order_text.config(state=tk.DISABLED)

    def complete_order(self) -> None:
        """Complete the current order and show receipt"""
        if self.order_processor.total_price <= 0:
            messagebox.showinfo("Empty Order", "Please add items to your order first.")
            return

        # Get receipt text and queue number
        receipt_text = self.order_processor.get_receipt_text()
        queue_number = self.order_processor.get_next_ticket_number()

        # Create receipt window
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Receipt")
        receipt_window.geometry("500x500")

        # Add receipt content
        receipt_frame = tk.Frame(receipt_window, padx=20, pady=20)
        receipt_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(receipt_frame, text="RECEIPT", font=("Arial", 18, "bold")).pack(pady=(0, 10))

        # Receipt text
        receipt_area = tk.Text(receipt_frame, font=("Courier", 10), width=60, height=20)
        receipt_area.pack(pady=10)
        receipt_area.insert(tk.END, receipt_text)
        receipt_area.insert(tk.END, f"\nQueue number ticket: {queue_number}")
        receipt_area.config(state=tk.DISABLED)

        # Close button
        tk.Button(
            receipt_frame,
            text="Close Receipt",
            font=("Arial", 12),
            command=lambda: [receipt_window.destroy(), self.reset_order()]
        ).pack(pady=10)

    def reset_order(self) -> None:
        """Reset the current order"""
        # Create a new OrderProcessor with the same menu
        self.order_processor = OrderProcessor(self.menu)
        # Update display
        self.update_order_display()

    def exit_program(self) -> None:
        """Exit the program"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
