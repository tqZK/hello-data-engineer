import argparse
from urllib import parse

import numpy as np
import pandas as pd

URL_CUSTOM_SEPARATOR = "|"
URL_CUSTOM_TIMESTAMP_PREFIX = "<134>"
USER_MIN_EVENTS = 2


def read_input_file(input_path):
    """
    Reads input files and returns its data as pd.DataFrame
    """
    with open(input_path, 'r') as file:
        content = file.read().splitlines()
    return pd.DataFrame(data=content, columns=['url_orig'])


def parse_url(url):
    """
    Parses single url (str) and returns dict with information needed from this url
    """
    url_parts = url.split(URL_CUSTOM_SEPARATOR)
    query = url_parts[4].split("?")[-1]
    query_dict = parse.parse_qs(query)
    return {
        "timestamp": pd.to_datetime(url_parts[2].lstrip(URL_CUSTOM_TIMESTAMP_PREFIX)),
        "user_id": url_parts[3],
        "article_id": query_dict.get("a", [np.nan])[0],
        "wiki_id": query_dict.get("c", [np.nan])[0]
    }


def parse_input_data(df):
    """
    Parses pd.DataFrame (with original url) and returns pd.DataFrame with parts of url as columns
    """
    return df['url_orig'].apply(lambda url: pd.Series(parse_url(url)))


def is_same_wiki_and_article(row):
    """
    Analyses input row (event) and returns dict with information whether user first and last event was logged
    on the same wiki and article. Parameter `row` could be dict or pd.Series.
    Article ids are unique only for a single wiki.
    """
    is_same_article = False
    is_same_wiki = False
    if row["wiki_id_last"] == row["wiki_id_first"]:
        is_same_wiki = True
        if row["article_id_last"] == row["article_id_first"]:
            is_same_article = True
    return {
        "is_same_article": is_same_article,
        "is_same_wiki": is_same_wiki,
        "user_id": row["user_id"]
    }


def process_data(df):
    """
    Processes pd.DataFrame with url info to return a pd.DataFrame that will hold information if given user
    visited the same wiki and article in first and last events.
    """
    # filters users that had less than USER_MIN_EVENTS events.
    df_filtered = df.groupby('user_id').filter(lambda x: len(x) >= USER_MIN_EVENTS)
    df_grouped = df_filtered.groupby('user_id')
    columns_to_keep = ['user_id', 'article_id', 'wiki_id']
    # retrieves rows with max and min timestamp, merges them on user_id
    # and applies is_same_wiki_and_article() on each row to return final df
    return df_filtered.loc[df_grouped["timestamp"].idxmin(), columns_to_keep].merge(
        df_filtered.loc[df_grouped["timestamp"].idxmax(), columns_to_keep],
        on="user_id",
        suffixes=("_first", "_last")
    ).apply(lambda row: pd.Series(is_same_wiki_and_article(row)), axis=1)


def save_output_file(output_path, df):
    """
    Saves pd.DataFrame to given output_path in CSV format.
    """
    df.sort_values(by=['user_id']).to_csv(output_path, index=False)


def parse_clickstream_logs(input_path, output_path):
    """
    Runs whole pipeline of functions
    """
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
