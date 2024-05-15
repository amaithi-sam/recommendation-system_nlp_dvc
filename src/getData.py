import argparse
import yaml
import os
import pandas as pd


def read_params(config_path):
    with open(config_path) as file:
        config = yaml.safe_load(file)

    return config


def get_dataframe(config_path):
    config = read_params(config_path)

    raw_data_path = config["data_source"]["raw_data_source"]
    data_sample = config["data_source"]["data_sample"]

    df = pd.read_csv(raw_data_path, sep=",", index_col='index')

    return df.sample(n=data_sample)


# if __name__ == "__main__":
#     args = argparse.ArgumentParser()
#     args.add_argument("--config", default="params.yaml")
#     parsed_args = args.parse_args()
