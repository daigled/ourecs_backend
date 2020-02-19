import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
        
dynamodb = boto3.resource("dynamodb", region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

table = dynamodb.Table('ourecs_artists')



def lambda_handler(event, context):
    
    print("**** here's the event path parameters! ***")
    print(event['pathParameters'])
    
    
    
    artistName = event['pathParameters']['artistName']
    
    try:
        response = table.get_item(
            Key={
                'name': artistName
            }    
        )
    except ClientError as e:
        response = e
    else:
        item = response['Item']
        return {
            'statusCode': 200,
            'body': json.dumps(item, indent=4, cls=DecimalEncoder)
        }
    
    
