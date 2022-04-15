import datetime
import copy
import json


def create_config(occupancy_template, months_into_future, s3_output_path, metadata_path):
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    config = copy.deepcopy(occupancy_template)
    config["request_config"]["variables"]["request"]["count"] = months_into_future
    config["request_config"]["variables"]["request"]["month"] = current_month
    config["request_config"]["variables"]["request"]["year"] = current_year
    config['out_config']['s3_path'] = s3_output_path
    config['metadata_config']['s3_path'] = metadata_path
    return config


def create_occupancy_configs(s3, occupancy_template, months_into_future, out_path, s3_output_path, metadata_path):
    configs = [create_config(occupancy_template, months_into_future, s3_output_path, metadata_path)]
    configs = {"configs": configs}
    with s3.open(out_path, "w") as f:
        json.dump(configs, f, indent=4)