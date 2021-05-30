import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')

def translate_function(text, source, target):
    
    response = translate.translate_text(
    Text = text,
    SourceLanguageCode = source,
    TargetLanguageCode = target
    )
    
    return response

def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    #translate text
    text = result['Item']['text']
    lang =  event['pathParameters']['language']
    text = translate_function(text, "auto", lang)
    
    result['Item']['text'] = text['TranslatedText']


    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response