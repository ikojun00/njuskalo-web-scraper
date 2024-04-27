import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv('csv/info/info.csv')
    
    for index, row in df.iterrows():
        if row['Price'] < 1000 or row['Living area'] < 10:
            df = df.drop(index)
        elif row['Price'] < 10000:
            df.at[index, 'Price'] = row['Price'] * row['Living area']
        print(index)

    df.to_csv('bla.csv', index=False)
