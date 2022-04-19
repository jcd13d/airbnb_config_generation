import numpy as np
import json
import os


def id_list_to_config(ids, num_ids_per_container):
    ids = np.array(ids)

    total_listings = len(ids)
    num_containers = (np.ceil(total_listings/num_ids_per_container))

    ids2 = np.pad(ids, (0, int(num_containers*num_ids_per_container) - total_listings))
    ids2 = ids2.reshape(-1, num_ids_per_container)
    print(f"Resulting configuration: {ids2.shape[0]} containers running {ids2.shape[1]} IDs each.")

    ids2 = ids2.tolist()
    ids2 = [list(filter((0.0).__ne__, x)) for x in ids2] # filter out pad zeros
    return ids2, num_containers


def create_batch_submission_config(batch_job_template, num_containers, duration):
    batch_job_template["arrayProperties"]["size"] = int(num_containers)
    batch_job_template["timeout"]["attemptDurationSeconds"] = duration
    return batch_job_template


def create_batch_event_config(eventbridge_template, num_containers):
    eventbridge_template["Targets"][0]["BatchParameters"]["ArrayProperties"]["Size"] = int(num_containers)
    return eventbridge_template


def get_ids_from_dir(s3, directory):
    files = s3.ls(directory)
    files = [f"s3://{x}" for x in files]
    ids = []
    for file in files:
        with s3.open(file, "r") as f:
            tmp = json.load(f)['ids']

        ids = ids + tmp

    return ids


def create_id_configs(s3, batch_job_template, eventbridge_template, num_ids_per_container, id_list_location, out_path, duration):

    ids = get_ids_from_dir(s3, id_list_location)

    list_of_id_lists, num_containers = id_list_to_config(ids, num_ids_per_container)

    sub_config = create_batch_submission_config(batch_job_template, num_containers, duration)

    event_config = create_batch_event_config(eventbridge_template, num_containers)

    with s3.open(os.path.join(out_path, "batch_array_job_sub.json"), "w") as f:
        json.dump(sub_config, f, indent=4)

    with s3.open(os.path.join(out_path, "eventbridge/eventbridge_id_target.json"), "w") as f:
        json.dump(event_config, f, indent=4)

    with s3.open(os.path.join(out_path, "id_config.json"), "w") as f:
        json.dump({"id_configs": list_of_id_lists}, f, indent=4)


