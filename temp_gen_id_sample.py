import json
import numpy as np


if __name__ == "__main__":
    np.random.seed(0)
    with open("config/config_local.json", "r") as f:
        config = json.load(f)

    with open(config['id_config']['id_list_location'], "r") as f:
        ids = json.load(f)['ids']

    NUM_IDS = 2000

    print(len(ids))

    ids = np.array(ids)

    ids = np.random.choice(ids, replace=False, size=NUM_IDS, )
    print(len(ids))
    print(list(ids))
    ids = list(ids)

    with open("dat/ids_miami.json", "w") as f:
        json.dump({"ids": ids}, f, indent=4)

