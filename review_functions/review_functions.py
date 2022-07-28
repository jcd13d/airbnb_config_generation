import datetime
import copy
import json


def create_config(review_template, reviews_limit, s3_output_path, metadata_path):
    config = copy.deepcopy(review_template)
    config["request_config"]["variables"]["request"]["limit"] = reviews_limit
    config['out_config']['s3_path'] = s3_output_path
    config['metadata_config']['s3_path'] = metadata_path
    return config


def create_review_configs(s3, review_template, reviews_limit, out_path, s3_output_path, metadata_path):
    configs = [create_config(review_template, reviews_limit, s3_output_path, metadata_path)]
    configs = {"configs": configs}
    with s3.open(out_path, "w") as f:
        json.dump(configs, f, indent=4)