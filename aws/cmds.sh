# create log group if not already made, can select existing one in task def config
aws logs create-log-group --log-group-name  test-group-cli

# create clsuter if not already made
aws ecs create-cluster --cluster-name fargate-cluster

# create s3 bucket if needed
aws s3api create-bucket --bucket airbnb-scraper-bucket-0.0.1

# create task definition
aws ecs register-task-definition --cli-input-json file://aws/task_def.json

# use these to find values for next command
aws ec2 describe-security-groups
aws ec2 describe-subnets
aws ec2 describe-vcps

# for running task on fargate cluster
aws ecs run-task --cluster test-cli-fargate --task-definition config-creator --network-configuration "awsvpcConfiguration={subnets=[subnet-05ae50b3be2cd836e],securityGroups=[sg-02cd4994ba07e9848],assignPublicIp=ENABLED}" --launch-type FARGATE
# this one for btd
aws ecs run-task --cluster fargate-cluster --task-definition config-creator --network-configuration "awsvpcConfiguration={subnets=[subnet-0560d0f903be012ef],securityGroups=[sg-020c8eccdbd68453e],assignPublicIp=ENABLED}" --launch-type FARGATE
aws ecs run-task --cluster test-cli-fargate --task-definition scraper-1 --network-configuration "awsvpcConfiguration={subnets=[subnet-05ae50b3be2cd836e],securityGroups=[sg-02cd4994ba07e9848],assignPublicIp=ENABLED}" --launch-type FARGATE


# create ECR Repo
aws ecr create-repository \
    --repository-name config-creator \
    --image-scanning-configuration scanOnPush=true \
    --region us-east-1 >> ./aws/ecr_repo_rsponse.json


aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 033046933810.dkr.ecr.us-east-1.amazonaws.com
docker buildx build --platform=linux/amd64 -t config-creator .
docker tag config-creator:latest 033046933810.dkr.ecr.us-east-1.amazonaws.com/config-creator:latest
docker push 033046933810.dkr.ecr.us-east-1.amazonaws.com/config-creator:latest

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 443188464014.dkr.ecr.us-east-1.amazonaws.com
docker buildx build --platform=linux/amd64 -t config-creator .
docker tag config-creator:latest 443188464014.dkr.ecr.us-east-1.amazonaws.com/config-creator:latest
docker push 443188464014.dkr.ecr.us-east-1.amazonaws.com/config-creator:latest


aws s3 cp /Users/justindiemmanuele/Documents/projects/airbnb_scraper/miami_ids.json s3://jd-s3-test-bucket9/master_configs/ids.json
aws s3 cp /Users/justindiemmanuele/Documents/projects/airbnb_scraper/miami_ids.json s3://airbnb-scraper-bucket-0.0.1/master_configs/ids/ids.json

aws s3 cp config s3://airbnb-scraper-bucket-0.0.1/master_configs/ --recursive

# chron job run every day at 1AM EST
aws events put-rule --name "daily-config-creator-job" --schedule-expression "cron(0 4 * * ? *)"
aws events put-targets --rule "daily-config-creator-job" --cli-input-json file://aws/eventbridge_target.json



zip ./function.zip ./function.py

aws lambda create-function --function-name update-functions \
--zip-file fileb://function.zip --handler function.handler --runtime python3.8 \
--role arn:aws:iam::443188464014:role/lambda-eventbridge-full-access --timeout 20

./build/build.sh

aws lambda update-function-configuration --function-name launch-postprocessor --handler aws.function.handler

aws lambda update-function-code --function-name update-functions --zip-file fileb://function.zip

aws lambda invoke --function-name update-functions --payload '{"test": "hello"}' response.txt --cli-binary-format raw-in-base64-out

aws s3 cp remote_created_configs/eventbridge/eventbridge_id_target.json s3://airbnb-scraper-bucket-0-0-1/running_configs/eventbridge/eventbridge_id_target.json

 aws s3 cp remote_created_configs/batch_array_job_sub.json  s3://airbnb-scraper-bucket-0-1-1/running_configs/batch_array_job_sub.json

aws lambda invoke --function-name test-container-lambda --payload '{"test": "hello"}' response.txt --cli-binary-format raw-in-base64-out

spark-submit --packages io.delta:delta-core_2.12:2.0.0 --py-files s3://airbnb-scraper-bucket-0-0-1/postprocessing_files/dependencies.zip s3://airbnb-scraper-bucket-0-0-1/postprocessing_files/postprocessing.py