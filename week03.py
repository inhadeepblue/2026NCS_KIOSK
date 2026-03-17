import pandas as pd

items = [
    [100, 95, 70],
    [80, 75, 100],
    [90, 85, 99]
]
df_items = pd.DataFrame(items, index=[1, 2, 3], columns=['a', 'b', 'c'])
print(df_items)