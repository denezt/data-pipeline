#!/bin/bash

# Clone minio-py
git clone https://github.com/minio/minio-py

# Add current location to stack
pushd .

# Change to project directory
if [ -d "minio-py" ];
then
	cd minio-py
	sudo python setup.py install
fi

# Go back to original location
popd

# Create virtual environment
if [ ! -d "minio-venv" ];
then
	printf "\033[36mCreating, virtual environment...\033[0m\n"
	python -m "minio-venv"
fi
