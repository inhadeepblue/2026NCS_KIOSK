class CafeOrder:
    DISCOUNT_THRESHOLD = 10000
    DISCOUNT_RATE = 0.1

    def __init__(self, drinks, prices):
        self.drinks = drinks
        self.prices = prices
        self.amounts = [0] * len(drinks)
        self.total_price = 0

    def apply_discount(self, price: int) -> float:
        """
        Apply discount rate when the total amount exceeds a certain threshold
        :param price: price before discount
        :return: price after discount
        """
        if price >= self.DISCOUNT_THRESHOLD:
            return price * (1 - self.DISCOUNT_RATE)
        return price

    def process_order(self, idx: int):
        """
        Process the order and accumulate the total price
        :param idx: index of the ordered drink
        """
        print(f"{self.drinks[idx]} ordered. Price: {self.prices[idx]} won")
        self.total_price += self.prices[idx]
        self.amounts[idx] += 1

    def display_menu(self) -> str:
        """
        Generate a dynamic menu string
        :return: formatted menu string
        """
        return "".join(
            [f"{k + 1}) {self.drinks[k]} {self.prices[k]} won  "
             for k in range(len(self.drinks))]
        ) + f"{len(self.drinks) + 1}) Exit : "

    def print_summary(self):
        """Print order summary and final price"""
        print("\nProduct\tPrice\tAmount\tSubtotal")
        for i in range(len(self.drinks)):
            if self.amounts[i] > 0:
                print(f"{self.drinks[i]}\t{self.prices[i]}\t{self.amounts[i]}\t"
                      f"{self.prices[i] * self.amounts[i]}")

        discounted_price = self.apply_discount(self.total_price)
        discount = self.total_price - discounted_price

        print(f"\nTotal price before discount: {self.total_price} won")
        if discount > 0:
            print(f"Discount amount: {discount:.0f} won")
            print(f"Total price after discount: {discounted_price:.0f} won")
        else:
            print("No discount applied")
            print(f"Total price: {self.total_price} won")

    def run(self):
        """Execute the order system"""
        while True:
            try:
                menu = int(input(self.display_menu()))
                if 1 <= menu <= len(self.drinks):
                    self.process_order(menu - 1)
                elif menu == len(self.drinks) + 1:
                    print("Order finished~")
                    break
                else:
                    print(f"Menu {menu} is invalid. Please choose from the above menu.")
            except ValueError:
                print("Please enter a valid number. Try again.")

        self.print_summary()


if __name__ == "__main__":
    # menu_drinks = ["Ice Americano", "Cafe Latte", "Watermelon Juice"]
    # menu_prices = [2000, 3000, 4900]
    menu_drinks = ["Ice Americano", "Cafe Latte"]
    menu_prices = [2000, 3000]
    cafe = CafeOrder(menu_drinks, menu_prices)
    cafe.run()