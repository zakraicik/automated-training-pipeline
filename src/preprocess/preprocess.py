import argparse
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def preprocess(input_data_path, output_data_path):
    column_names = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
    ]

    logger.info(f"input_data_path:  {input_data_path}:")

    df = pd.read_csv(input_data_path, header=None, names=column_names)

    df = df.dropna(subset=["species"])

    encoder = LabelEncoder()
    df["species"] = encoder.fit_transform(df["species"])

    df = df[["species"] + [col for col in df if col != "species"]]

    train, test = train_test_split(df, test_size=0.2, random_state=42)

    mean_train = train.mean()

    train.fillna(mean_train, inplace=True)
    test.fillna(mean_train, inplace=True)

    scaler = StandardScaler()
    scaler.fit(train[["sepal_length", "sepal_width", "petal_length", "petal_width"]])

    train[
        ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    ] = scaler.transform(
        train[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    )
    test[
        ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    ] = scaler.transform(
        test[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    )

    train.to_csv(
        os.path.join(output_data_path, "train_data.csv"), header=False, index=False
    )
    test.to_csv(
        os.path.join(output_data_path, "test_data.csv"), header=False, index=False
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", type=str)
    parser.add_argument("--output-data", type=str)
    args = parser.parse_args()

    preprocess(args.input_data, args.output_data)
