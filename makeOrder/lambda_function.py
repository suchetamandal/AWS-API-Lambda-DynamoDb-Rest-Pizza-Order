from __future__ import print_function

import boto3
import json
import sys

def lambda_handler(event, context):
    menu_id = event.get('menu_id')
    order_id = event.get('order_id')
    c_name = event.get('customer_name')
    c_mail = event.get('customer_email')

    try:
        #Connect to dynamo db
        dynamodb = boto3.resource('dynamodb',region_name='us-west-2')
        order = dynamodb.Table('Order')
        order.put_item(Item=event)    
        return selectType(dynamodb, order, event)
    except:
        return "500 Server Error"
        

def selectType(dynamodb, order, event):
    menu = dynamodb.Table('Menu')
    selectedMenu = menu.get_item(Key={
        'menu_id':event.get('menu_id')
    })
    orderDetails = order.get_item(Key={
        'order_id':event.get('order_id')
    })
    orderStatus =''
    orderStatus = orderDetails['Item'].get('order_status')
    
    sequence = selectedMenu['Item'].get('sequence')
    selection = selectedMenu['Item'].get('selection')
    size = selectedMenu['Item'].get('size')
    
    #If there is no specified seqnce and size then craete a dummy pattern
    if sequence == None:
        sequence = ["selection","size"]
    if selection == None:
        selection = ["Cheese","Pepperoni"]
    if size == None:
        size = ["Slide", "Small", "Medium", "Large", "X-Large"]

    nextStep = calculateNextStep(orderStatus, sequence)
    sys.stdout.write("Status Updated"+str(nextStep))
    #Update the sequence Data in order table
    order.update_item(
        Key={
            'order_id': event.get('order_id')
        },
        UpdateExpression='SET order_status = :val1',
        ExpressionAttributeValues={
            ':val1': nextStep
        })
        
    sys.stdout.write("Status Updated")
    if nextStep == 'selection':
        counter = 1
        selectionText = ""
        for s in selection:            
            selectionText = selectionText + " " + str(counter) + ". " + s + ","
            counter = counter + 1

        response = {} 
        response.setdefault("Message", "Hi " + event.get('customer_name') + ", " + "please choose one of these selection: " + selectionText )
        return response
        
    elif nextStep == 'size':
        counter =1
        selectionText = ""
        for s in size:            
            selectionText = selectionText + " " + str(i) + ". " + s + ","
            counter = counter + 1

        response = {} 
        response.setdefault("Message", "Which size do you want?: " +selectionText )
        sys.stdout.write(response)
        return json.dumps(response) 
        
    elif nextStep == 'summary':
        return;    
        
def calculateNextStep(orderStatus, sequence):
    if orderStatus == None:
        return sequence[0]
        
    for k,v in enumerate(sequence):
        if (k+1) == len(sequence):
            sys.stdout.write("Summary")
            return "summary"
        elif seq == orderStatus:
            sys.stdout.write(sequence[i+1])
            return sequence[i+1]    