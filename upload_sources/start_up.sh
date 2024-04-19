#!/bin/bash

# Starting Virtual Environment
source minio-venv/bin/activate

# Executing converter and uploading to s3 drive
for process in 'converting_and_cleaning.py' 'upload_data.py';
do
	python "${process}"
done

# Deactivating and exiting out
# of Virtual Environment
deactivate
