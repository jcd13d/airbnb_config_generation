# Usage
This is meant to be a one-stop-shop where configure files can be updated and 
pushed to AWS to control the airbnb scraper infrastructure. Ideally, we narrow 
the inputs down to the few knobs we may want to turn at any given time. The 
main config file is [config.json](config/config.json) which controls:
* pricing scraper template location
* availability scraper template location
* aws batch template location
* eventbridge template location
* pricing scraper configuration
  * how many days of pricing do we want to pull into the future
  * where to output configuration for pricing scraper
  * where to write outputs from scraper
  * where to write metadata generated by scraping run
* availability scraper configuration
  * start month and how many months into future to scrape
  * where to output configuration for availability scraper
  * where to write outputs from scraper
  * where to write metadata generated by scraping run
* configuration for creating list of IDs to run
  * number of IDs per container
  * location of master list of IDs
  * where to write config to 
  * max duration of scraping job

The file [generate_id_scraper_configs.py](generate_id_scraper_configs.py) is
the "main" function and will use the templates and [config.json](config/config.json)
to create the needed configurations and write them to their rightful s3 locations. 
This is run on a recurring basis from a lambda function to ensure that configs are
up-to-date before the ID scrapers are run. In theory, if we want to make on-the-fly 
changes to the infrastructure, we should be able to update the configs here then 
push them using
```commandline
./bin/push_master_configs.sh
```


# Setup
* Configure AWS CLI
* Create ECR repo
* Push container to ECR repo
* Create ECS cluster if you don't already have one
* Create necessary IAM roles
  * ecsTaskExecutionRole
    * AmazonS3FullAccess
    * AmazonECSTaskExecutionRolePolicy
  * AmazonECSTaskS3BucketRole
    * AmazonECSTaskS3BucketPolicy
      * s3 accesses for bucked (I use full access)
* Update Task definition with the correct URIs
* Create task definition
* Create s3 bucket if needed
* Update master configs, templates if needed
* Upload master configs
* Run task definitio



Switched to running container in lambda since couldnt schedule
ecs, seems to work just testing, try to schedule
working on schedule thru lambda, can also get lambda to start 
an ECS task if we want. Probably fine as lambda for now

updated to include emr config, havent built/psuhed/tested