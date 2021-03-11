import argparse
from urllib import parse

import numpy as np
import pandas as pd

COLUMNS_TO_SAVE = ["user_id", "is_same_article", "is_same_wiki"]


def read_input_file(input_path):
    with open(input_path, 'r') as file:
        content = file.readlines()
    return pd.DataFrame(data=content, columns=['url_orig'])


def parse_url(url):
    url_parts = url.split("|")
    query = url_parts[4].split("?")[-1]
    query_dict = parse.parse_qs(query)
    return {
        "url": url_parts[0],
        "lang": url_parts[1],
        "timestamp": pd.to_datetime(url_parts[2].lstrip("<134>")),
        "user_id": url_parts[3],
        "article_id": query_dict.get("a", [np.nan])[0],
        "wiki_id": query_dict.get("c", [np.nan])[0]
    }


def parse_input_data(df):
    return pd.concat([df, df.url_orig.apply(lambda url: pd.Series(parse_url(url)))], axis=1)


def is_same_wiki_and_article(row):
    is_same_article = False
    is_same_wiki = False
    if row["wiki_id_last"] == row["wiki_id_first"]:
        is_same_wiki = True
        if row["article_id_last"] == row["article_id_first"]:
            is_same_article = True
    return {
        "is_same_article": is_same_article,
        "is_same_wiki": is_same_wiki
    }


def process_data(df):
    df_filtered = df.groupby('user_id').filter(lambda x: len(x) > 2)
    df_grouped = df_filtered.groupby('user_id')
    columns_to_keep = [
        'user_id',
        'article_id',
        'wiki_id'
    ]
    df_user_events = df_filtered.loc[df_grouped["timestamp"].idxmin(), columns_to_keep].merge(
        df_filtered.loc[df_grouped["timestamp"].idxmax(), columns_to_keep],
        on="user_id",
        suffixes=("_first", "_last")
    )
    df_final = pd.concat([
        df_user_events,
        df_user_events.apply(lambda row: pd.Series(is_same_wiki_and_article(row)), axis=1)
    ], axis=1)
    return df_final


def save_output_file(output_path, df):
    df.sort_values(by=['user_id']).to_csv(output_path, columns=COLUMNS_TO_SAVE)


def parse_clickstream_logs(input_path, output_path):
    df = read_input_file(input_path)
    df = parse_input_data(df)
    df = process_data(df)
    save_output_file(output_path, df)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clistream logs parser')
    parser.add_argument('--input_path', type=str, help='Path to input log file')
    parser.add_argument('--output_path', type=str, default="output.csv",
                        help='Path to output CSV file (default: output.csv)')
    args = parser.parse_args()
    parse_clickstream_logs(args.input_path, args.output_path)
