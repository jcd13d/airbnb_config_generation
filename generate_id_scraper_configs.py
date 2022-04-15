from price_functions.price_functions import create_price_configs
from occupancy_functions.occupancy_functions import create_occupancy_configs
from id_functions.create_id_config import create_id_configs
import json
import s3fs


def main(s3, pricing_config, pricing_template_loc, occupancy_config, occupancy_template_loc, id_config, batch_template_loc):

    with s3.open(pricing_template_loc, "r") as f:
        pricing_template = json.load(f)
    with s3.open(occupancy_template_loc, "r") as f:
        occupancy_template = json.load(f)
    with s3.open(batch_template_loc, "r") as f:
        batch_template = json.load(f)

    create_price_configs(s3, pricing_template, **pricing_config)
    create_occupancy_configs(s3, occupancy_template, **occupancy_config)
    create_id_configs(s3, batch_template, **id_config)


if __name__ == "__main__":
    config_path = "s3://jd-s3-test-bucket9/master_configs/config.json"
    s3 = s3fs.S3FileSystem()

    with s3.open(config_path, "r") as f:
        config = json.load(f)

    main(s3, **config)

