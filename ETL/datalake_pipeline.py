import boto3
import os
from dotenv import load_dotenv
import gzip
import shutil
load_dotenv() 




def compress_file(file_path):
    gz_path = file_path + ".gz"
    with open(file_path, 'rb') as f_in:
        with gzip.open(gz_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return gz_path




def load_raw_layer(s3_client,file_path,platform):
    try:
        if not os.path.exists(file_path):
            print(f"ERROR AT LOAD RAW LAYER FILE NOT FOUND: {file_path}")
            return
        gz_path = compress_file(file_path)
        file_name = os.path.basename(gz_path)
        s3_client.upload_file(gz_path,BUCKET_NAME,f'raw/{platform}/{file_name}')
        print(f'****** SUCCESS LOAD DATA TO DATALAKE RAW LAYER: {os.path.basename(file_path)} ******')
        for f in [file_path, gz_path]:
            try:
                os.remove(f)
                print(f"🧹 Deleted local file: {f}")
            except Exception as e:
                print(f"Warning: Could not delete {f} → {e}")
    except Exception as e:
        print(f"****** ERROR WHEN LOAD DATA TO RAW LAYER DATALAKE: {e} ******")
    return



def load_bronze_layer():
    return



def load_silver_layer():
    return


def load_layer3():
    return


if __name__=='__main__':
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    if not BUCKET_NAME:
        print("EROOR: CANT FIND BUCKET_NAME.")
        exit()
    else:
        print('yes')
    s3_client = boto3.client('s3')
    load_raw_layer(s3_client=s3_client,file_path='C:/MY_PROJECT/Lazlytics---Lazada Product Analytics/RawData/Tiki/2025-10-30_1.json',platform='tiki')

        





