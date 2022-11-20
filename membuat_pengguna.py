from decouple import config
import boto3

client =  boto3.client('cognito-idp')
response = client.admin_create_user(
    UserPoolId=config('USER_POOL_ID'),
    Username='sarah',
    UserAttributes=[
        {
            'Name': 'custom:peran',
            'Value': 'staff'
        },
        {
            'Name': 'email',
            'Value': 'sarah@mailinator.com'
        }
    ],
    TemporaryPassword='rahasia',
    DesiredDeliveryMediums=[
        'EMAIL'
    ]
)

response = client.admin_set_user_password(
    UserPoolId=config('USER_POOL_ID'),
    Username='sarah',
    Password='rahasia',
    Permanent=True
)