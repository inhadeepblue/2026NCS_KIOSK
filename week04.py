import pandas as pd

items = {
    'a': [100, 80, 90],
    'b': [95, 75, 85],
    'c': [70, 100, 99]
}
df_items = pd.DataFrame(items, index=[1, 2, 3])
print(df_items)
print(df_items.apply(lambda n : n * n)) # Apply function to each object.