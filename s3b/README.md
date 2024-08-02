# S3B

This project is designed for encrypting directories and uploading them to Minio3 or other compatible S3 servers.

## Requirements

- Python 3.6+
- gnupg
- boto3
- PyInstaller (for creating a binary file)

## Installation

1. Install the required libraries:
    ```bash
    pip install gnupg boto3 pyinstaller
    ```

2. Create a GPG key if you don't have one yet:
    ```bash
    gpg --full-generate-key
    ```

3. Create a configuration file `config.json`:
    ```json
    {
        "directory": "/path/to/your/directory",
        "bucket": "your-bucket-name",
        "access_key": "your-access-key",
        "secret_key": "your-secret-key",
        "endpoint_url": "http://localhost:9000"
    }
    ```

## Usage

1. Run the script without encryption:
    ```bash
    python3 main.py /path/to/config.json
    ```

2. Run the script with encryption:
    ```bash
    python3 main.py /path/to/config.json -e recipient@example.com
    ```

## Creating a Binary File

1. Use PyInstaller to create a binary file:
    ```bash
    pyinstaller --onefile main.py
    ```

2. Move the binary file to `/usr/bin` for easy access:
    ```bash
    sudo mv dist/main /usr/bin/s3b
    sudo chmod +x /usr/bin/s3b
    ```

3. Run the binary file:
    ```bash
    s3b /path/to/config.json
    ```
