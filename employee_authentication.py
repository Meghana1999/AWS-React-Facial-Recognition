import boto3
# we can have good return object that front-end can use => json
import json

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodbTableName = 'employee'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
employeeTable = dynamodb.Table(dynamodbTableName)

bucketName = 'myapp-visitor-images'

def lambda_handler(event, context):
    print(event)
    # Set to queryStringParameters, we created objectKey , we have control over it
    objectKey = event['queryStringParameters']['objectKey']
    # Read image from S3 bucket
    # .read()=> tahts how we get bytes
    # Rekognition will expect a binary data types for the images to process
    image_bytes = s3.get_object(Bucket=bucketName, Key=objectKey)['Body'].read()
    response = rekognition.search_faces_by_image(
        # we need to use the same collection ID we have used in registration
        CollectionId = 'employees',
        Image={'Bytes':image_bytes}
    )

    # After response comes back, we are going to all the matching faces in the collection
    for match in response['FaceMatches']:
        # will print FaceID, along with Confidence score
        print(match['Face']['FaceID'], match['Face']['Confidence'])

        # Now we check with our database if any of the faces matches
        face = employeeTable.get_item(
            Key={
                'rekognitionId': match['Face']['FaceId']
            }
        )

        if 'Item' in face:
            print('Person Found: ', face['Item'])
            return buildResponse(200, {
                'Message': 'Success',
                'firstName': face['Item']['firstName'],
                'lastName':face['Item']['lastName']
            })
    
    print('Person could not be Recognized')
    return buildResponse(403, {'Message':'Person Not Found'})

def buildResponse(statusCode, body=None):
    response = {
    'statusCode': statusCode,
    # Access-Control-Allow-Origin => we call this API from our React App
    'headers':{
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
    }
    }
    if body is not None:
        response['body'] = json.dumps(body)
    
    # Going to return the response object to the client
    return response
