import argparse
import os
import pandas as pd


def preprocess(input_data_path, output_data_path):
    # Load the dataset
    df = pd.read_csv(input_data_path, header=None)

    # TODO: Any preprocessing you want to apply to the Iris dataset.
    # This can include normalization, encoding, data cleaning, etc.

    # Save the preprocessed data
    df.to_csv(output_data_path, header=False, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", type=str)
    parser.add_argument("--output-data", type=str)
    args = parser.parse_args()

    preprocess(args.input_data, args.output_data)
