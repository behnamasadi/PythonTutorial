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
