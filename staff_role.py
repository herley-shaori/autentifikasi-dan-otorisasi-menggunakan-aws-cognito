from decouple import config
from pycognito import Cognito
import boto3
import json

u = Cognito(user_pool_id=config('USER_POOL_ID'),client_id=config('CLIENT_ID'),client_secret=config('CLIENT_SECRET'),username='sarah')
u.authenticate(password='rahasia')

idToken = u.id_token

client = boto3.client('cognito-identity')
logins = {
        "cognito-idp.%s.amazonaws.com/%s"%(config('REGION'),config('USER_POOL_ID')): idToken
    }

response = client.get_id(
    AccountId=config('ACCOUNT_ID'),
    IdentityPoolId=config('IDENTITY_POOL_ID'),
    Logins=logins
)

response = client.get_credentials_for_identity(
    IdentityId=response['IdentityId'],
    Logins=logins
)

sesi = boto3.Session(region_name = config('REGION'),
aws_access_key_id=response['Credentials']['AccessKeyId'],
aws_secret_access_key=response['Credentials']['SecretKey'],
aws_session_token=response['Credentials']['SessionToken'])
s3 = sesi.client('s3')

# Daftar semua s3 bucket.
# print(json.dumps(s3.list_buckets(),sort_keys=True, indent=3,default=str))

# Daftar objek di random-string bucket.
# for key in s3.list_objects(Bucket='random-string')['Contents']:
#     print(json.dumps(key,sort_keys=True,indent=3,default=str))
# print('---------------------------------------------------------------------')

# Unduh berkas.
with open('berkas_dari_s3_staff.txt', 'wb') as f:
    s3.download_fileobj('random-string', 'haloo.txt', f)

# print(idToken)
    