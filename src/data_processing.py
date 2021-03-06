import argparse
import os
from random import shuffle

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from load_data import read_params


def coding_target(df, target):
    label = LabelEncoder()
    df[[target]] = label.fit_transform(np.ravel(df[[target]]))
    return df


def split_data(
    df, target, train_data_path, test_data_path, split_ratio, random_state
):
    df = coding_target(df, target)
    train, test = train_test_split(
        df, test_size=split_ratio, random_state=random_state, shuffle=True
    )
    train.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")
    test.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")


def split_and_saved_data(config_path):
    """
    split the train dataset(data/raw) and save it in the data/processed folder
    input: config path
    output: save splitted files in output folder
    """
    config = read_params(config_path)
    raw_data_path = config["raw_data_config"]["raw_data_csv"]
    test_data_path = config["processed_data_config"]["test_data_csv"]
    train_data_path = config["processed_data_config"]["train_data_csv"]
    split_ratio = config["raw_data_config"]["train_test_split_ratio"]
    random_state = config["raw_data_config"]["random_state"]
    raw_df = pd.read_csv(raw_data_path)
    target = config["raw_data_config"]["target"]
    split_data(
        raw_df,
        target,
        train_data_path,
        test_data_path,
        split_ratio,
        random_state,
    )


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)
