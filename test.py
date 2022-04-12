import pandas as pd



df = pd.read_parquet("dat")
print(df.columns)
print(df)

print(df[df['id'] == 23069234])