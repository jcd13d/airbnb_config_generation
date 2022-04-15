import datetime
import json
import copy


def get_dates_from_days_in_future(day_list):
    today = datetime.datetime.now()
    day_strings = []

    for day_num in day_list:
        day_strings.append((today + datetime.timedelta(days=day_num)).strftime("%Y-%m-%d"))

    return day_strings


def get_config_days(days_into_future, skip_days):
    if skip_days:
        raise ValueError("Skip days not implemented")
    else:
        return get_dates_from_days_in_future([i for i in range(days_into_future)])


def get_day_config(config_template, start_day, end_day, s3_output_path, metadata_path):
    config_template = copy.deepcopy(config_template)
    config_template["request_config"]["variables"]["pdpSectionsRequest"]["checkIn"] = start_day
    config_template["request_config"]["variables"]["pdpSectionsRequest"]["checkOut"] = end_day
    config_template["out_config"]["s3_path"] = s3_output_path
    config_template["metadata_config"]["s3_path"] = metadata_path
    return config_template


def create_price_configs(s3, config_template, skip_days, days_into_future, s3_output_path, out_path, metadata_path):
    pricing_configs = []
    days_to_config = get_config_days(days_into_future, skip_days)
    for start, end in zip(days_to_config[:-1], days_to_config[1:]):
        pricing_configs.append(get_day_config(config_template, start, end, s3_output_path, metadata_path))

    configs = {"configs": pricing_configs}
    with s3.open(out_path, "w") as f:
        json.dump(configs, f, indent=4)