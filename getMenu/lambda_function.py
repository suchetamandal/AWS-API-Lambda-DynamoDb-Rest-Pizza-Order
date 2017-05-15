from __future__ import print_function

import boto3
import json
import sys
import decimal
import collections

print('Loading function')

## Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    menu_id = event.get('menu_id')
    #Connect to dynamo db
    dynamodb = dynamodb = boto3.resource('dynamodb',region_name='us-west-2')
    table = dynamodb.Table('Menu')
    response = table.get_item(
        Key={
            'menu_id': menu_id
        }
    )
    store_hours = collections.OrderedDict()
    store_hours['Mon'] = response['Item']['store_hours']['Mon']
    store_hours['Tue'] = response['Item']['store_hours']['Tue']
    store_hours['Wed'] = response['Item']['store_hours']['Wed']
    store_hours['Thu'] = response['Item']['store_hours']['Thu']
    store_hours['Fri'] = response['Item']['store_hours']['Fri']
    store_hours['Sat'] = response['Item']['store_hours']['Sat']
    store_hours['Sun'] = response['Item']['store_hours']['Sun']
    
    res = response['Item']
    res['store_hours'] = store_hours
    return res

