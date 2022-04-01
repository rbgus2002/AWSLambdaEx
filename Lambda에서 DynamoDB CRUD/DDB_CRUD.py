import boto3
import json
from botocore.exceptions import ClientError


def put_element(electronics, brand, memorySize, isBreaked):  # put item to dynamoDB ([C]RUD)
    dynamodb = boto3.resource('dynamodb')  # dynamoDB connect

    try:
        response = dynamodb.Table('Electronics').put_item(
            Item={
                'Kind': electronics,
                'Brand': brand,
                'information': {
                    'memorySize': memorySize,
                    'isBreaked': isBreaked
                }
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response


def update_element(electronics, brand, memorySize, isBreaked):  # update existing item to dynamoDB (CR[U]D)
    dynamodb = boto3.resource('dynamodb')

    try:
        response = dynamodb.Table('Electronics').update_item(
            Key={'Kind': electronics, 'Brand': brand},
            UpdateExpression="SET information= :values",
            ExpressionAttributeValues={
                ':values': {'memorySize': memorySize, 'isBreaked': isBreaked}
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response


def get_element(electronics, brand):  # (C[R]UD)
    dynamodb = boto3.resource('dynamodb')

    try:
        response = dynamodb.Table('Electronics').get_item(Key={'Kind': electronics, 'Brand': brand})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response


def delete_element(electronics, brand):  # (CRU[D])
    dynamodb = boto3.resource('dynamodb')

    try:
        response = dynamodb.Table('Electronics').delete_item(
            Key={'Kind': electronics, 'Brand': brand}
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response


def lambda_handler(event, context):
    # electronics_put_response = put_element('Sub Battery', 'Xiaome', '0GB', True)
    # electronics_update_response = update_element('IPAD', 'apple', '512GB', True)
    # electronics_get_response = get_element('IPAD', 'apple')
    # electronics_delete_response = delete_element('IPAD', 'apple')

    try:
        if event is not None:
            json_data = json.dumps(event)
            dict = json.loads(json_data)

            if dict['type'] is None:
                print('event type empty')
            else:
                for datum in dict['data']:
                    electronics = datum['Kind']
                    brand = datum['Brand']
                    isBreaked = datum['information'].get('isBreaked')
                    memorySize = datum['information'].get('memorySize')

                if (dict['type'] == 'put'):
                    test_put_response = put_element(electronics, brand, isBreaked, memorySize)
                    print(test_put_response)

                elif (dict['type'] == 'update'):
                    test_update_response = update_element(electronics, brand, isBreaked, memorySize)
                    print(test_update_response)

                elif (dict['type'] == 'delete'):
                    test_delete_response = delete_element(electronics, brand)
                    print(test_delete_response)

                elif (dict['type'] == 'get'):
                    test_get_response = get_element(electronics, brand)
                    print(test_get_response)

                else:
                    print('"type" is error in event')

        else:
            print('event empty')

    except ClientError as e:
        print(e.response['Error'])

    return "success"

'''
event object (json type) 

{
  "type": "get",
  "data": [
    {
      "Kind": "Magic Mouse",
      "Brand": "apple",
      "information": {
        "isBreaked": false,
        "memorySize": "0GB"
      }
    }
  ]
}
'''