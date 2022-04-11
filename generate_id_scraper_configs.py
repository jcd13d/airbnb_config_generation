from price_functions.price_functions import create_price_configs
from occupancy_functions.occupancy_functions import create_occupancy_configs
from id_functions.create_id_config import create_id_configs
import json


def main(pricing_config, pricing_template_loc, occupancy_config, occupancy_template_loc, id_config, batch_template_loc):

    with open(pricing_template_loc, "r") as f:
        pricing_template = json.load(f)
    with open(occupancy_template_loc, "r") as f:
        occupancy_template = json.load(f)
    with open(batch_template_loc, "r") as f:
        batch_template = json.load(f)

    create_price_configs(pricing_template, **pricing_config)
    create_occupancy_configs(occupancy_template, **occupancy_config)
    create_id_configs(batch_template, **id_config)


if __name__ == "__main__":
    config_path = "config/config.json"

    with open(config_path, "r") as f:
        config = json.load(f)

    main(**config)

