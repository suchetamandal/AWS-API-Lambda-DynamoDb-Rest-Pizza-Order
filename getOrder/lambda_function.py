from __future__ import print_function

import boto3
import json

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
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        tableOrder = dynamodb.Table('Order')
        response = tableOrder.get_item(Key={
            'order_id':event.get('order_id')
            })        

        res = {
            "menu_id": response['Item'].get('menu_id'),
            "order_id": response['Item'].get('order_id'),
            "customer_name": response['Item'].get('customer_name'),
            "customer_email": response['Item'].get('customer_email'),
            "order_status": response['Item'].get('order_status'),
            "order": {
                "selection": response['Item'].get('selection'),
                "size": response['Item'].get('size'),
                "costs": response['Item'].get('costs'),
                "order_time": response['Item'].get('order_time')
            }
        }

        return res

    except:

        return "500 Server Error"