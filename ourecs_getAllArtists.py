import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
table = dynamodb.Table('ourecs_artists')

def lambda_handler(event, context):
    
    response = table.scan()
    
    items = response["Items"]

    return {
        'statusCode': 200,
        'body': json.dumps(items, indent=4)
    }
