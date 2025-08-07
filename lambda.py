import json
import boto3
import time

# Initialize DynamoDB and SES client
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='ap-south-1')  # Make sure you set the correct SES region

# DynamoDB table
table = dynamodb.Table('subscribers')  # Make sure the table name matches your DynamoDB table

def send_welcome_email(email, name):
    """Function to send a welcome email via SES"""
    try:
        subject = "Welcome to Our Newsletter!"
        body = f"Hello {name},\n\nThank you for subscribing to our newsletter! Stay tuned for updates and special offers."

        # Send email via SES
        response = ses.send_email(
            Source='anjisingam103@gmail.com',  # Make sure to replace with your verified email in SES
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        print(f"Email sent to {email}: {response}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def save_subscriber(data):
    """Lambda function to handle subscriber subscriptions"""
    name = data.get('name')  # Full name
    email = data.get('email')  # Email address

    if not name or not email:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Name and email are required'}),
            'headers': {'Content-Type': 'application/json'}
        }

    try:
        # Get current GMT time for subscription timestamp
        gmt_time = time.gmtime()
        now = time.strftime('%Y-%m-%d %H:%M:%S', gmt_time)

        # Save the subscriber to DynamoDB
        table.put_item(
            Item={
                'email': email,
                'name': name,
                'subscribedAt': now
            }
        )

        # Send a welcome email
        send_welcome_email(email, name)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Subscription successful for {name}'}),
            'headers': {'Content-Type': 'application/json'}
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to save subscriber: {str(e)}'}),
            'headers': {'Content-Type': 'application/json'}
        }

def lambda_handler(event, context):
    try:
        # Parse the event body
        body = json.loads(event.get('body', '{}'))
        
        # Directly call the save_subscriber function without the 'operation' check
        return save_subscriber(body)
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }

