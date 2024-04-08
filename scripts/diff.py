import pandas as pd
import csv


def compare_csv(new_links, old_links):
    df1 = pd.read_csv(new_links)
    df2 = pd.read_csv(old_links)

    set1 = set(map(tuple, df1.values))
    set2 = set(map(tuple, df2.values))

    diff_df1 = pd.DataFrame(list(set1 - set2), columns=df1.columns)
    diff_df2 = pd.DataFrame(list(set2 - set1), columns=df2.columns)

    return diff_df1, diff_df2


def delete_rows(csv_file):
    df = pd.read_csv(csv_file)
    for sold_url in sold_urls:
        df = df[df['Url'] != sold_url]

    df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    county = "osjecko-baranjska"
    sold_urls = []

    new_links = 'apartment_links.csv'
    old_links = f'csv/links/{county}_links.csv'

    diff_df1, diff_df2 = compare_csv(new_links, old_links)

    diff_df1.to_csv('new.csv', index=False)
    diff_df2.to_csv('sold.csv', index=False)

    with open('sold.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            sold_urls.extend(row)
            
    delete_rows(f'csv/info/{county}_info.csv')
