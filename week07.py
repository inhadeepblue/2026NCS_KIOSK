from typing import List  # type hint

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
            [f"{k + 1}) {self.drinks[k]} {self.prices[k]} won  "
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

    def __init__(self):
        """Initialization method for the OrderProcessor class."""
        self.total_price = 0
        self.amounts = []  # 메뉴 항목 수에 따라 초기화될 예정

    def apply_discount(self, price: int) -> float:
        """
        Apply discount rate when the total amount exceeds a certain threshold
        :param price: price before discount
        :return: price after discount
        """
        if price >= self.DISCOUNT_THRESHOLD:
            return price * (1 - self.DISCOUNT_RATE)
        return price

    def process_order(self, menu: Menu, idx: int) -> None:
        """
        Process the order and accumulate the total price
        :param menu: Menu object (dependency)
        :param idx: index of the ordered drink
        """
        drink_name = menu.get_drink_name(idx)
        drink_price = menu.get_price(idx)

        print(f"{drink_name} ordered. Price: {drink_price} won")
        self.total_price += drink_price
        self.amounts[idx] += 1

    def print_receipt(self, menu: Menu) -> None:
        """Print order summary and final price with formatted alignment using f-string"""
        print(f"\n{'Product':<15} {'Price':<10} {'Amount':<10} {'Subtotal':<10}")
        print("-" * 50)

        for i in range(menu.get_menu_length()):
            if self.amounts[i] > 0:
                drink_name = menu.get_drink_name(i)
                drink_price = menu.get_price(i)

                print(
                    f"{drink_name:<15} {drink_price:<10} {self.amounts[i]:<10} {drink_price * self.amounts[i]:<10}")

        discounted_price = self.apply_discount(self.total_price)
        discount = self.total_price - discounted_price

        print("-" * 50)
        print(f"{'Total price before discount:':<30} {self.total_price:>5}")
        if discount > 0:
            print(f"{'Discount amount:':<30} {discount:<10.0f}")
            print(f"{'Total price after discount:':<30} {discounted_price:<10.0f}")
        else:
            print(f"{'No discount applied.':<30}")
            print(f"{'Total price:':<30} {self.total_price:>5}")

    def run(self, menu: Menu):
        """Execute the order system"""
        self.amounts = [0] * menu.get_menu_length() # run 시점에 메뉴 길이에 맞춰 초기화

        while True:
            try:
                menu_display = menu.display_menu()
                choice = int(input(menu_display))
                if 1 <= choice <= menu.get_menu_length():
                    self.process_order(menu, choice - 1)
                elif choice == menu.get_menu_length() + 1:
                    print("Order finished~")
                    break
                else:
                    print(f"Menu {choice} is invalid. Please choose from the above menu.")
            except ValueError:
                print("Please enter a valid number. Try again.")
            except IndexError as e:
                print(e)  # Display the specific IndexError message

        self.print_receipt(menu)


if __name__ == "__main__":
    menu_drinks = ["Ice Americano", "Cafe Latte", "Watermelon Juice"]
    menu_prices = [2000, 3000, 4900]

    menu = Menu(menu_drinks, menu_prices)
    order_processor = OrderProcessor() # Menu 객체를 생성하지 않음
    order_processor.run(menu) # run 메서드에 Menu 객체를 전달