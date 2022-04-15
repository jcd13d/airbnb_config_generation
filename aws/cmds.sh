# create task definition
aws ecs register-task-definition --cli-input-json file://aws/task_def.json


# use these to find values for next command
aws ec2 describe-security-groups
aws ec2 describe-subnets
aws ec2 describe-vcps

# for running task on fargate cluster
aws ecs run-task --cluster test-cli-fargate --task-definition config-creator --network-configuration "awsvpcConfiguration={subnets=[subnet-05ae50b3be2cd836e],securityGroups=[sg-02cd4994ba07e9848],assignPublicIp=ENABLED}" --launch-type FARGATE
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


aws s3 cp /Users/justindiemmanuele/Documents/projects/airbnb_scraper/miami_ids.json s3://jd-s3-test-bucket9/master_configs/ids.json