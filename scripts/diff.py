import pandas as pd
import csv

def compare_csv(new_links, old_links):
    df1 = pd.read_csv(new_links)
    df2 = pd.read_csv(old_links)

    new_diff_df = pd.DataFrame(columns=df1.columns)
    old_diff_df = pd.DataFrame(columns=df2.columns)

    for _, row in df1.iterrows():
        if not (df2 == row).all(axis=1).any():
            new_diff_df = pd.concat([new_diff_df, row.to_frame().T], ignore_index=True)

    for _, row in df2.iterrows():
        if not (df1 == row).all(axis=1).any():
            old_diff_df = pd.concat([old_diff_df, row.to_frame().T], ignore_index=True)

    return new_diff_df, old_diff_df


def delete_rows(csv_file, urls):
    df = pd.read_csv(csv_file, encoding='utf-8')
    for url in urls:
        df = df[df['Url'] != url]

    df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    county = "zagrebacka"
    urls = []

    old_links = f'csv/links/counties/{county}_links.csv'
    new_links = f'{county}_links.csv'

    new_diff_df, old_diff_df = compare_csv(new_links, old_links)

    new_diff_df.to_csv(f'{county}_new.csv', index=False)
    old_diff_df.to_csv(f'{county}_sold.csv', index=False)

    with open(f'{county}_sold.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            urls.append(row[2])

    delete_rows(f'csv/info/counties/{county}_info.csv', urls)
