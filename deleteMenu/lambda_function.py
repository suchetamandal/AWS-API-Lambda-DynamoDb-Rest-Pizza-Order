from __future__ import print_function

import boto3
import json
import sys 

print('Loading function')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    #Connect to dynamo db
    dynamodb = dynamodb = boto3.resource('dynamodb',region_name='us-west-2')
    table = dynamodb.Table('Menu')
    menu_id = event.get('menu_id')
    try:
        
        res = table.delete_item(
            Key={
                'menu_id': menu_id
            }
        )
        return respond(False,"200 OK")
    except:
        return "500 Server Error"
