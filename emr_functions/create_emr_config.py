
def create_emr_configs(s3, emr_template, version, master_instance_type, slave_instance_type, instance_count, steps, bootstrap):
    emr_template["ReleaseLabel"] = version
    emr_template["Instances"]["MasterInstanceType"] = master_instance_type
    emr_template["Instances"]["SlaveInstanceType"] = slave_instance_type
    emr_template["Instances"]["InstanceCount"] = instance_count
    emr_template["Steps"] = steps
    emr_template["BootstrapActions"] = bootstrap
    return emr_template


