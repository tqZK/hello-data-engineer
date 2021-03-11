import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clistream logs parser')
    parser.add_argument('--input_path', type=str, help='Path to input log file')
    parser.add_argument('--output_path', type=str, default="output.csv",
                        help='Path to output CSV file (default: output.csv)')
    main_args = parser.parse_args()
    print(main_args)
