### What is a `DataFrame`?

A `DataFrame` is a two-dimensional, size-mutable, and heterogeneous tabular data structure with labeled axes (rows and columns) in `pandas`. You can think of it like an in-memory spreadsheet or SQL table, or even a dict of Series objects.


### Creating a DataFrame:

There are many ways to create a DataFrame. Here's one of the simplest ways using a dictionary:

```python

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'San Francisco', 'Los Angeles']
}

df = pd.DataFrame(data)
```

This will give:

```
      Name  Age           City
0    Alice   25       New York
1      Bob   30  San Francisco
2  Charlie   35    Los Angeles
```

or you can simply create:

```
df = pd.DataFrame(columns=["Name", "Article", "Quantity"])
```

### Basic Operations:

You can do a variety of operations on DataFrames:

1. **Viewing data:** `df.head()` (top rows) and `df.tail()` (bottom rows).
2. **Selecting columns:** `df['Name']` or `df[['Name', 'Age']]`.
3. **Filtering rows:** `df[df['Age'] > 30]`.
4. **Merging/Joining data:** `pd.merge(df1, df2, on='key_column')`.
















import pandas as pd
import numpy as np

print("##################### create dataframe #####################")

df = pd.DataFrame(columns=["Name", "Article", "Quantity"])

print("##################### append columns to an empty DataFrame #####################")
df['Name'] = ['Tv', 'PC', 'Desk']
df['Article'] = [97, 600, 200]
df['Quantity'] = [2200, 75, 100]
print(df)


print("##################### iterate rows #####################")
for index, row in df.iterrows():
    print(index, row['Name'])


print("##################### append rows #####################")
df_new_row = pd.DataFrame(
    {'Name': ['Fridge'], 'Article': [97], 'Quantity': [2200]})
df = pd.concat([df, df_new_row])


print(df)


print("##################### printing headers (columns names) #####################")
cols = df.columns.tolist()
print("columns are: ", cols)
print("head: ", df.head())


print("##################### accessing rows by index #####################")
print("the value of column Name at row index 1:", df.loc[1, ['Name']])

print("##################### updating rows #####################")
df.at[1, 'Name'] = 'new value'
print("the value of column Name at row index 1 after update is:",
      df.loc[1, ['Name']])

print("##################### updating rows in loop #####################")

for index in df.index:
    df.loc[index, ['Name']] = "*" + df.loc[index, ['Name']] + "*"

print(df)

print("##################### delete columns #####################")
# or df.pop("temp") or del df["temp"]
df.drop('Quantity', inplace=True, axis=1)
print('removing the Quantity column')
print(df)


print("##################### rename columns #####################")
df.rename(columns={'Article': 'New-Article'}, inplace=True)
print(df)

print("##################### reset index column #####################")
#df = df.reset_index(drop=True)
df.set_index('Name', inplace=True)
print(df)

print("##################### remove index when writhing to csv #####################")
df.to_csv('data/tmp.csv', index=False)

print("##################### read csv #####################")
df = pd.read_csv("data/tmp.csv", index_col=False)
print(df)


[code](../Tutorials/pandas_snipets.py)  
