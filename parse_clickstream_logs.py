import argparse
from urllib import parse

import pandas as pd


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


def process_data(data):
    pass


def save_output_file(output_path, data):
    pass


def parse_clickstream_logs(input_path, output_path):
    data = read_input_file(input_path)
    data = parse_input_file(data)
    data = process_data(data)
    save_output_file(output_path, data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clistream logs parser')
    parser.add_argument('--input_path', type=str, help='Path to input log file')
    parser.add_argument('--output_path', type=str, default="output.csv",
                        help='Path to output CSV file (default: output.csv)')
    args = parser.parse_args()
    parse_clickstream_logs(args.input_path, args.output_path)
