import json
from utils import get_gift_details, generate_suggestion


def handler(event, context):
    query_params = event['queryStringParameters']

    if query_params is None:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': {}
        }
    else:
        occasion = query_params.get('occasion', 'birthday')
        price = query_params.get('price', '50')
        age = query_params.get('age', '30')
        relationship = query_params.get('relationship', 'spouse')
        hobby = query_params.get('hobby', 'reading')

    # Call OpenAI function to generate gift suggestions
    openaiResponse = generate_suggestion(
        f'3 {occasion} gifts in JSON list format {{gift: gift idea, explanation: reason for purchase}} with price {price} for my {age} year old {relationship} who likes {hobby}'
    )

    gifts = get_gift_details(openaiResponse)

    # Return response in the required format
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'gifts': gifts})
    }
    return response
