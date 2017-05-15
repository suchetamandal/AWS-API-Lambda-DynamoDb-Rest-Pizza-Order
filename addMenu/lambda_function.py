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
    store_name = event.get('store_name')
    selection = event.get('selection')
    size = event.get('size')
    price = event.get('price')
    store_hours = event.get('store_hours')
    
    #Connect to dynamo db
    dynamodb = dynamodb = boto3.resource('dynamodb',region_name='us-west-2')
    table = dynamodb.Table('Menu')
    
    try:
        
        res = table.put_item(
            Item={
                'menu_id': menu_id,
                'store_name': store_name,
                'selection' : selection,
                'size' : size,
                'price' : price,
                'store_hours': store_hours
            }
        )
        return respond(False,"200 OK")
    
    except:
        return "500 Server Error"
