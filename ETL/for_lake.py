import boto3
from botocore.client import Config
from keys import *
import os

key_id=datalake_key['keyID']
key_name=datalake_key['keyName']
application_key=datalake_key['applicationKey']
endpoint=datalake_key['Endpoint']



def load_datalake_bronze(local_dir):
    s3=boto3.client(
    "s3",
    endpoint_url=endpoint,
    aws_access_key_id=key_id,
    aws_secret_access_key=application_key,
    config=Config(signature_version="s3v4")
    )
    bucket_name='Lazlytics-DataLake'
    for filename in os.listdir(local_dir):
        local_path = os.path.join(local_dir, filename)
        object_key = f"RawData/Lazada/2025-09-11/{filename}"
        s3.upload_file(local_path, bucket_name, object_key)
        print(f"✅ Uploaded {filename} → {object_key}")
    return

def load_datalake_layer2():
    return

def load_datalake_layer3():
    return


if __name__=='__main__':
    pass