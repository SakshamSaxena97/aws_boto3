import boto3
from botocore.exceptions import ClientError

region = 'us-east-1'
user = "" #insert your access key to use when creating the client
pw = "" #insert the secret key to use when creating the client
client = boto3.client(service_name = 'ses', 
                        region_name = region, 
                        aws_access_key_id = user, 
                        aws_secret_access_key = pw)
me = ''
you = ''
SUBJECT = 'testSUBJECT'
# COMMASPACE = ', '
# you = COMMASPACE.join(you)
#Build email message parts

#Build and send email
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                "This email was sent with Amazon SES using the "
                "AWS SDK for Python (Boto)."
                )

BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK for Python)</h1>
    Test MailAKIAIESYK4C5PDH6FTVA
    </body>
    </html>
      """ 
CHARSET = "UTF-8"
try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                you,
            ]
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=me,
        # If you are not using a configuration set, comment or delete the
        # following line
        # ConfigurationSetName=CONFIGURATION_SET,
    )
# # Display an error if something goes wrong.	
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])