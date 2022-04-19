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