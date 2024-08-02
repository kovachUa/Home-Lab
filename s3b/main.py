import os
import tarfile
import hashlib
import boto3
import subprocess
import argparse
import json

def create_archive(directory, archive_path):
    with tarfile.open(archive_path, 'w:gz') as tar:
        tar.add(directory, arcname=os.path.basename(directory))

def encrypt_file(file_path, recipient):
    encrypted_file_path = file_path + '.gpg'
    try:
        subprocess.run(
            ['gpg', '--output', encrypted_file_path, '--encrypt', '--recipient', recipient, file_path],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error encrypting file {file_path}: {e}")
        raise
    return encrypted_file_path

def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def upload_to_s3(bucket_name, file_path, access_key, secret_key, endpoint_url, object_name=None):
    s3_client = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    if object_name is None:
        object_name = os.path.basename(file_path)
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Error uploading file {file_path}: {e}")

def process_directory(directory, bucket_name, access_key, secret_key, endpoint_url, recipient=None):
    archive_path = directory + '.tar.gz'
    create_archive(directory, archive_path)

    if recipient:
        encrypted_file_path = encrypt_file(archive_path, recipient)
        file_hash = get_file_hash(encrypted_file_path)
        object_name = os.path.basename(archive_path) + '.gpg'
        os.remove(archive_path)  # Видаляємо оригінальний архів
    else:
        encrypted_file_path = archive_path
        file_hash = get_file_hash(archive_path)
        object_name = os.path.basename(archive_path)
    
    print(f"File: {encrypted_file_path}, Hash: {file_hash}")
    upload_to_s3(bucket_name, encrypted_file_path, access_key, secret_key, endpoint_url, object_name)
    if recipient:
        os.remove(encrypted_file_path)  # Видаляємо зашифрований архів після завантаження

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and upload directories to Minio3 with optional GPG encryption')
    parser.add_argument('json_file', type=str, help='Path to the JSON file with parameters')
    parser.add_argument('-e', '--encrypt', type=str, help='GPG recipient for encryption (optional)', default=None)
    
    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        params = json.load(f)
    
    process_directory(
        params['directory'],
        params['bucket'],
        params['access_key'],
        params['secret_key'],
        params['endpoint_url'],
        args.encrypt
    )
