import pandas as pd

items = [
    [100, 95, 70],
    [80, 75, 100],
    [90, 85, 99]
]
df_items = pd.DataFrame(items, index=[1, 2, 3], columns=['a', 'b', 'c'])
print(df_items)
df_items_melt = pd.melt(df_items).rename(columns={'variable':'var', 'value':'val'}).query('val >= 85')
print(df_items_melt)

