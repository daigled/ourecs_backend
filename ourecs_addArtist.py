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

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
table = dynamodb.Table('ourecs_artists')


def lambda_handler(event, context):
      
    body = json.loads(event['body'])
    
    try:
        response = table.put_item(
            Item={
                'name': body['name'],
                'albums': []
            }
        )
        
        responseMessage = "artist " + body['name'] + " successfully added"
        
        return {
            'statusCode': 200,
            'body': responseMessage
        }
    except ClientError as e:
        response = e
        return {
            'statusCode': 500,
            'body': json.dumps(e)
        }
    



    