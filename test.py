import pandas as pd



df = pd.read_parquet("dat")
print(df.columns)

print(df[df['id'] == 6774081])