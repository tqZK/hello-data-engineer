import argparse
import pandas as pd


def read_input_file(input_path):
    with open(input_path, 'r') as file:
        content = file.readlines()
    return pd.DataFrame(data=content, columns=['url'])


def parse_input_file(data):
    pass


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