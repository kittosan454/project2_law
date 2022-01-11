import pandas as pd
import glob

data_paths = glob.glob('./crawling/*')
print(data_paths)
df = pd.read_csv("./crawling/casenum_-49-0.csv", index_col=0)
print(df.head())

for data_path in data_paths:
    df_temp = pd.read_csv(data_path)
    df = pd.concat([df, df_temp], axis = 1)

df.dropna(inplace=True)
# df.reset_index(drop=True, inplace=True) #인덱스 재정렬git push -u origin master


print(df.head())
print(df.tail())
print(df.info())

df.to_csv('./all_laws.csv', index=False)