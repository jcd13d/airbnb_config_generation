import boto3
import json


client = boto3.client('events')
s3 = boto3.resource('s3')

def handler(event, context):
    print(event)
    content_object = s3.Object('airbnb-scraper-bucket-0-0-1', 'running_configs/eventbridge/eventbridge_id_target.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')
    cfg = json.loads(file_content)

    response = client.put_targets(
        Rule=cfg['Rule'],
        Targets=cfg['Targets']
    )
    return response