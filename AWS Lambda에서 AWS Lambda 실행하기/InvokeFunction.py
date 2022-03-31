import json
import boto3

connect = boto3.client(service_name = 'lambda', region_name = 'ap-northeast-2')
connect.invoke(FunctionName = '부르길 원하는 함수', InvocationType='Event', Payload=json.dumps('event로서 넘겨주길 원하는 인자 (dictionary)'))