from __future__ import print_function

import boto3
import json
import sys

print('Loading function')


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
    dynamodb = boto3.resource('dynamodb',region_name='us-west-2')
    table = dynamodb.Table('Menu')
    
    table.update_item(
    Key={
        'menu_id': event.get('menu_id')
    },
    UpdateExpression='SET selection = :val1',
    ExpressionAttributeValues={
        ':val1': event.get('selection')
    })
    
    return "200 OK"
