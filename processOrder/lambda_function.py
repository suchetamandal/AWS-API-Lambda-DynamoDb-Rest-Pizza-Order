from __future__ import print_function

import boto3
import json
import sys
from datetime import datetime

print('Loading function')


def lambda_handler(event, context):
    try:
        dynamodb = dynamodb = boto3.resource('dynamodb',region_name='us-west-2')
        order = dynamodb.Table('Order')
        order_id = event.get('order_id')
        orderDetails = order.get_item(
            Key={
                'order_id': order_id
            }
        )
        orderStatus = orderDetails['Item'].get('order_status') 
        menu_id = orderDetails['Item'].get('menu_id')
        menu = dynamodb.Table('Menu')
        menuDetails = menu.get_item(
            Key={
                'menu_id': menu_id
            }
        )
        sequence = menuDetails['Item'].get('sequence')
        selection = menuDetails['Item'].get('selection')
        size = menuDetails['Item'].get('size')
        price = menuDetails['Item'].get('price')
        if sequence == None:
            sequence = ["selection","size"]
        if selection == None:
            selection = ["Cheese","Pepperoni"]
        if size == None:
            size = ["Slide", "Small", "Medium", "Large", "X-Large"]
        if price == None:
            price = ["3.50", "7.00", "10.00", "15.00", "20.00"]
   
        if orderStatus == 'selection':
            order.update_item(
                Key={
                    'order_id': event.get('order_id')
                },
                UpdateExpression='SET selection = :val1',
                ExpressionAttributeValues={
                    ':val1': selection[int(event.get('input'))-1]
                }
            )
        elif orderStatus == 'size':
            order.update_item(
                Key={
                    'order_id': event.get('order_id')
                },
                UpdateExpression='SET size = :val1',
                ExpressionAttributeValues={
                    ':val1': size[int(event.get('input'))-1]
                }
            )
            
        updatedOrder = order.get_item(Key={
            'order_id': order_id
        })
        
        nextStatus = calculateNextStep(sequence, orderStatus)
 
        order.update_item(
            Key={
                'order_id': updatedOrder['Item'].get('order_id')
            },
            UpdateExpression='SET order_status = :val1',
            ExpressionAttributeValues={
                ':val1': nextStatus
            }
        )
        
        if nextStatus == 'selection':
            s = ""
            for i, sel in enumerate(selection):            
                s = s + " " + str(i+1) + ". " + sel + ","

            res = {} 
            res.setdefault("Message", "Hi " + event.get('customer_name') + ", " + "please choose one of these selection: " +s )
            return res
            
        elif nextStatus == 'size':
            s = ""
            for i, si in enumerate(size):            
                s = s + " " + str(i+1) + ". " + si + ","

            res = {} 
            res.setdefault("Message", "Which size do you want?: " +s )
            return res
            
        elif nextStatus == 'processing':
            response = order.get_item(Key={
                'order_id':updatedOrder['Item'].get('order_id')
            })

            #Get the size index in menu. same index needs to be used in price.
            i = 0
            for ss in size:
                if ss == response['Item'].get('size'):                
                    break
                i = i+1
            order.update_item(
                Key={
                    'order_id': event.get('order_id')
                },
                UpdateExpression='SET costs = :val1',
                ExpressionAttributeValues={
                    ':val1': price[i]
                }
            )
            sys.stdout.write("Now Price is "+str(price[i]))
            order.update_item(
                Key={
                    'order_id': event.get('order_id')
                },
                UpdateExpression='SET order_time= :val1',
                ExpressionAttributeValues={
                    ':val1': datetime.now().strftime('%Y-%m-%d@%H:%M:%S')
                }
            )
            sys.stdout.write("Now status is Ready")
            
            res = "Message: Your order costs $"+ price[i]+". We will email you when the order is ready. Thank you!"
            
            return res    
    except:
        return "Not Done"
        
def calculateNextStep(sequence, statusOrder):
    sys.stdout.write(str(statusOrder))
    if statusOrder == None:
        return sequence[0]
    for i, seq in enumerate(sequence):
        if (i+1) == len(sequence):
            return "processing"
        elif seq == statusOrder:
            return sequence[i+1]          