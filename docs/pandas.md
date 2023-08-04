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

or you can simply create an empty DataFram:

```
df = pd.DataFrame(columns=["Name", "Article", "Quantity"])
```

### append columns to an empty DataFrame 
```
df['Name'] = ['Tv', 'PC', 'Desk']
df['Article'] = [97, 600, 200]
df['Quantity'] = [2200, 75, 100]
```


#### iterate rows
```
for index, row in df.iterrows():
    print(index, row['Name'])
```

### append rows
```
df_new_row = pd.DataFrame(
    {'Name': ['Fridge'], 'Article': [97], 'Quantity': [2200]})
df = pd.concat([df, df_new_row])
```


### printing headers (columns names)
```
cols = df.columns.tolist()
print("columns are: ", cols)
print("head: ", df.head())
```


### Basic Operations:

You can do a variety of operations on DataFrames:


### selecting columns

```
df['Name']
```
or

```
df[['Name', 'Age']]
```

### filtering rows
```
df[df['Age'] > 30]
```

### merging/ joining data

```
pd.merge(df1, df2, on='key_column')
```

### accessing rows by index
```
print("the value of column Name at row index 1:", df.loc[1, ['Name']])
```
### updating rows
```
df.at[1, 'Name'] = 'new value'
print("the value of column Name at row index 1 after update is:",
      df.loc[1, ['Name']])
```
### updating rows in loop
```
for index in df.index:
    df.loc[index, ['Name']] = "*" + df.loc[index, ['Name']] + "*"
```


### delete columns
```
# or df.pop("temp") or del df["temp"]
df.drop('Quantity', inplace=True, axis=1)
print('removing the Quantity column')
print(df)
```

### rename columns
```
df.rename(columns={'Article': 'New-Article'}, inplace=True)
```

### reset index column
```
df = df.reset_index(drop=True)
df.set_index('Name', inplace=True)
print(df)
```
### remove index when writhing to csv
```
df.to_csv('data/tmp.csv', index=False)
```
### read csv 
```
df = pd.read_csv("data/tmp.csv", index_col=False)
print(df)
```


### processing data without iterating

In Pandas, it's often recommended to avoid explicit iteration (e.g., with `for` loops) over DataFrame rows or Series elements. Iterating over DataFrame rows using methods like `iterrows()` or `itertuples()` can be quite slow. Instead, one should leverage Pandas' built-in vectorized operations, which are optimized for performance.

Here are some common ways to process data in Pandas without iterating:

### 1. **Vectorized Operations**

For arithmetic operations, you can apply them directly to the whole DataFrame or Series.

```python
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df['A'] = df['A'] * 2
```

### 2. **Using `apply()`**

You can apply a function along the axis of a DataFrame.

```python
def some_function(x):
    return x * x

df['A'] = df['A'].apply(some_function)
```
or some lambda function:

```python
df["age"]=df["age"].apply(lambda x:x*2)
```

### 3. **Using `map()` for Series**

The `map()` function is used to map each value in a Series to some other value.

```python
s = pd.Series(['cat', 'dog', 'mouse'])
s = s.map(str.upper)
```

### 4. **Boolean Indexing**

You can filter rows based on some condition without iterating.

```python
df_filtered = df[df['A'] > 2]
```

### 5. **Using `where()`**

The `where()` function is used to replace values in rows or columns based on some condition.

```python
df['A'] = df['A'].where(df['A'] > 2, 0)
```

### 6. **Using `assign()` for Creating New Columns**

```python
df = df.assign(C = df['A'] + df['B'])
```

### 7. **String Operations with `str` Accessor**

You can apply string operations directly on a Series without iterating.

```python
df['text_column'] = df['text_column'].str.lower()
```

### 8. **Datetime Operations with `dt` Accessor**

If you have a datetime column, you can extract components without iterating.

```python
df['year'] = df['date_column'].dt.year
```

### 9. **Aggregation Functions**

Aggregation functions like `sum()`, `mean()`, `max()`, etc., are inherently vectorized.

```python
total = df['A'].sum()
```

### 10. **Using `eval()` for Computation**
`eval()` apply an string operation on the variable. For large DataFrames, `eval()` can be faster than standard operations.

```python
df.eval('age=age+quantity', inplace=True)
```

The key takeaway is that Pandas provides numerous built-in functionalities that allow you to perform operations on entire columns or DataFrames at once. By leveraging these capabilities, you can make your code cleaner, more concise, and often much faster.



### iloc
 `iloc` stands for "integer-location" and is used primarily for selecting rows and columns in a DataFrame by their integer index positions. 

Here's a basic overview:

1. **Single Selection**
    ```python
    import pandas as pd
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    })

    # Select the value in the first row and first column
    value = df.iloc[0, 0]  # returns 1
    ```

2. **Selecting Rows**
    ```python
    # Select the first row
    first_row = df.iloc[0]

    # Select the first and second rows
    first_two_rows = df.iloc[0:2]
    ```

3. **Selecting Columns**
    ```python
    # Select the first column
    first_column = df.iloc[:, 0]

    # Select the first and second columns
    first_two_columns = df.iloc[:, 0:2]
    ```

4. **Selecting Multiple Rows and Columns**
    ```python
    # Select the first two rows and the first two columns
    subset = df.iloc[0:2, 0:2]
    ```

5. **Using Lists**
    ```python
    # Select the first and third rows and the first and third columns
    subset = df.iloc[[0, 2], [0, 2]]
    ```

6. **Conditional Selection (using boolean indexing)**
    While `iloc` doesn't support boolean indexing directly, we can achieve this by combining it with boolean indexing on the dataframe:
    ```python
    mask = df['A'] > 1  # Boolean mask where column 'A' is greater than 1
    filtered_rows = df[mask]

    # Using iloc on the filtered dataframe
    subset = filtered_rows.iloc[:, 0:2]
    ```

Remember, `iloc` uses integer-based indexing, so it doesn't consider named indices (row labels) or column labels, unlike `loc` which is label-based indexing. If you try to access an index or column that doesn't exist, you will get an `IndexError`. Ensure that the indices you're using are valid for the DataFrame you're working with.
