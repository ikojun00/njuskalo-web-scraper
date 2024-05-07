import pandas as pd
import csv

def compare_csv(new_links, old_links):
    df1 = pd.read_csv(new_links)
    df2 = pd.read_csv(old_links)

    new_diff_df = pd.DataFrame(columns=df1.columns)
    old_diff_df = pd.DataFrame(columns=df2.columns)
    price_diff_df = pd.DataFrame(columns=df1.columns)
    date_diff_df = pd.DataFrame(columns=df1.columns)

    for _, row in df1.iterrows():
        url = row['Url']
        matching_row = df2[df2['Url'] == url]

        if matching_row.empty:
            new_diff_df = pd.concat([new_diff_df, pd.DataFrame([row])], ignore_index=True)
        else:
            if row['Price'] != matching_row['Price'].values[0]:
                price_diff_df = pd.concat([price_diff_df, pd.DataFrame([row])], ignore_index=True)
            if row['Date'] != matching_row['Date'].values[0]:
                date_diff_df = pd.concat([date_diff_df, pd.DataFrame([row])], ignore_index=True)

    for _, row in df2.iterrows():
        url = row['Url']
        matching_row = df1[df1['Url'] == url]

        if matching_row.empty:
            old_diff_df = pd.concat([old_diff_df, pd.DataFrame([row])], ignore_index=True)

    return new_diff_df, old_diff_df, price_diff_df, date_diff_df


# Deleting every row that is changed or sold in info
def delete_rows(csv_file, urls):
    df = pd.read_csv(csv_file, encoding='unicode_escape')
    for url in urls:
        df = df[df['Url'] != url]

    df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    county = "bjelovarsko-bilogorska"
    urls = []

    new_links = f'new_links.csv'
    old_links = f'{county}_links.csv'

    new_diff_df, old_diff_df, price_diff_df, date_diff_df = compare_csv(new_links, old_links)

    new_diff_df.to_csv(f'{county}_new.csv', index=False)
    old_diff_df.to_csv(f'{county}_sold.csv', index=False)
    price_diff_df.to_csv(f'{county}_price_diff.csv', index=False)
    date_diff_df.to_csv(f'{county}_date_diff.csv', index=False)

    with open(f'{county}_sold.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            urls.extend(row)

    with open(f'{county}_date_diff.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            urls.extend(row)

    with open(f'{county}_price_diff.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            urls.extend(row)

    delete_rows(f'{county}_info.csv', urls)
