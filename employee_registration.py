import boto3 # to call aws services

s3 = boto3.client('s3') # to call s3 buckets
rekognition = boto3.client('rekognition', region_name = 'us-east-1')
dynamodbTableName = 'employee' # our created table name
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Instantiate our employee table => in methods now we can use it directly
employeeTable = dynamodb.Table(dynamodbTableName)

# Define Handler => which takes in an event and context parameter
def lamda_handler(event, context):
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name'] # Getting bucket name
    # event => dictionary conatining event data passed to the lambda function
    # In this case, event contains source(S3 bucket)details, details about object that triggered the event.
    # S3 events contains multiple records, we  retrieve the first record
    # In that first record, we go to section 's3'
    #Then extracts the name of the S3 bucket

    key = event["Records"][0]['s3']['object']['key'] # Getting image name from Key
    # extracts the Key(object anme) of S3 object taht triggerd the event

    try:
        # generates unique rekognitionid and we save that into our dynamodb along with first, last name
        response = index_employee_image(bucket, key) 
        print(response)
        # even though we get response that doesnot mean indexing is succesful

        # Check for index succesful
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            # faceId => unique rekognitionid to identify people
            faceId = response['FaceRecords'][0]['Face']['FaceId']

            # Get employee first and last name from name of the image
            # Key going to have image name => Ex: Meghana_Nadella.jpeg
            # first split on . => separates base and extension , second split _ separates first, last name
            name = key.split('.')[0].split('_')
            firstName = name[0]
            lastName = name[1]
            register_employee(faceId, firstName, lastName) # saves to dynamodb
            return response




    except Exception as e:
        print(e)
        print('Error processing employee image {} from bucket{}'.format(key, bucket))
        raise e
    

def index_employee_image(bucket, key):
    response = rekognition.index_faces(
        # take in an image , reading from S3
        Image = {
            'S3Object':
            {
                'Bucket': bucket,
                'Name': key
            }
        },
        CollectionId = "employees"
    )
    return response

def register_employee(faceId, firstName, lastName):
    employeeTable.put_item(
        Item = {
            'rekognitionid': faceId,
            'firstName': firstName,
            'lastName': lastName

        }
    )