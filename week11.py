import tkinter as tk

def square(n):
    return n * n

def click_square():
    input_value = int(en_input.get())
    squared_input_value = square(input_value)
    lbl_display.config(text=f"{input_value} * {input_value} = {squared_input_value}")


def enter_key_square(ev):
    click_square()



root = tk.Tk()
root.geometry("400x300")

lbl_display = tk.Label(text="결과 디스플레이 창")
en_input = tk.Entry()
btn_calculate = tk.Button(text="제곱 연산", command=click_square)

en_input.bind("<Return>", enter_key_square)

lbl_display.pack()
en_input.pack(fill="x")
btn_calculate.pack(fill="x")

root.mainloop()