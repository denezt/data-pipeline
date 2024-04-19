#!/usr/bin/env python

import os
import json
import time

# file_uploader.py MinIO Python SDK example
from minio import Minio
from minio.error import S3Error
from configparser import ConfigParser

fp = open('settings/credentials.json','r')
strMinioClientInfo = fp.read()
mc_data = strMinioClientInfo.replace('\n','')
print(mc_data)
mc_object = json.loads(str(mc_data))

destUrl = mc_object['url']
accessKey = mc_object['accessKey']
secretKey = mc_object['secretKey']
# The file to upload, change this path if needed
config = ConfigParser()
config.read("settings/minio_api_setting.cfg")
dirname = config["source"]["directory"]

def main(targetUrl: str, accessKey: str, secretKey: str):
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(targetUrl, access_key=accessKey, secret_key=secretKey, secure=False)
    print(client)

    # The destination bucket and filename on the MinIO server
    bucket_name = "python-test-bucket"
    destination_files = [ "test-file-{}.txt".format(i) for i in range(1, 6) ]

    # Make the bucket if it doesn't exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the files, renaming it in the process
    for filename in destination_files:
        source_file = "/{}/{}".format(dirname, filename)
        client.fput_object(bucket_name, filename, source_file)
        print(source_file, "successfully uploaded as object", filename, "to bucket", bucket_name)

if __name__ == "__main__":
    try:
        print(destUrl, accessKey, secretKey)
        main(targetUrl=destUrl, accessKey=accessKey, secretKey=secretKey)
        print('Running, main application!')
    except S3Error as exc:
        print("error occurred.", exc)
