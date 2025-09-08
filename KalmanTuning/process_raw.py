import pandas as pd

df = pd.read_csv("./readings.csv")

print(df)
print("MEAN:")
print(df.mean())

print("STD:")
print(df.std())


print("VAR:")
print(df.var())