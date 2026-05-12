import tkinter as tk
import kiosk


class KioskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe Kiosk")

        # 메뉴 설정
        self.menu = kiosk.Menu(["Ice Americano", "Cafe Latte", "Watermelon Juice", "Ice tea"], [2000, 3000, 4900, 3300])
        self.order_processor = kiosk.OrderProcessor(self.menu)

        # 버튼 레이아웃
        self.buttons = []
        for i in range(self.menu.get_menu_length()):
            drink_name = self.menu.get_drink_name(i)
            drink_price = self.menu.get_price(i)
            btn = tk.Button(root, text=f"{drink_name}\n{drink_price} won", width=15, height=5,
                            command=lambda idx=i: self.order(idx))
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            self.buttons.append(btn)

        # 주문 완료 버튼
        self.complete_button = tk.Button(root, text="Finish Order", width=15, height=2, command=self.complete_order)
        self.complete_button.grid(row=self.menu.get_menu_length() // 2, column=0, columnspan=2, padx=10, pady=10)

        # 주문 출력 영역
        self.order_label = tk.Label(root, text="Order Summary", font=("Arial", 12), fg="blue")
        self.order_label.grid(row=self.menu.get_menu_length() // 2 + 1, column=0, columnspan=2, pady=10)

    def order(self, idx):
        drink_name = self.menu.get_drink_name(idx)
        self.order_processor.process_order(idx)
        self.order_label.config(text=f"Ordered: {drink_name}")

    def complete_order(self):
        self.order_processor.print_receipt()
        ticket_number = self.order_processor.get_next_ticket_number()
        self.order_label.config(text=f"Order Complete!\nQueue Number: {ticket_number}")


# GUI 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = KioskApp(root)
    root.mainloop()