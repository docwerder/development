import pathlib
import pandas as pd
import sys

print('gogo')
def load_and_normalize_df(patch_dir):
    exported_exchange_path = pathlib.Path(patch_dir) / "csv_file_reduced.csv"
    print("loading {exported_exchange_path} ...")
    exchange_file = pd.read_csv(exported_exchange_path)
    filtered_exchange_file = exchange_file
    filtered_exchange_file = filtered_exchange_file.reset_index()
    if "TYPE" in exchange_file.columns:
        exchange_file = exchange_file.rename(columns={'TYPE': 'type'})
    elif "type" in exchange_file.columns:
        exchange_file = exchange_file.rename(columns={'type': 'type'})
    else:
        raise ValueError("csv-File does not contain a 'TYPE' or 'type' namend column! ")

    return exchange_file, filtered_exchange_file


if __name__ == '__main__':

    sys.exit(app.exec_())

