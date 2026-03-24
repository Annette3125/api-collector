import logging
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

LOCAL_PATH = Path(os.getenv("LOCAL_PATH", "data/new/stock_data_latest.csv"))
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "")
S3_KEY = os.getenv("S3_KEY", "raw/stock_data_latest.csv")


def upload_latest_to_s3() -> bool:
    """
    Upload latest CSV to S3 (optional).
    Requires:
      - aws credentials configured (aws configure) OR IAM role
      - S3_BUCKET_NAME set in .env
    """
    if not BUCKET_NAME:
        logging.error("Missing S3_BUCKET_NAME in .env. Skipping upload.")
        return False

    if not LOCAL_PATH.exists():
        logging.error(f"Local file not found: {LOCAL_PATH}")
        return False

    s3_client = boto3.client("s3")

    try:
        logging.info(f"Uploading {LOCAL_PATH} to s3://{BUCKET_NAME}/{S3_KEY}")
        s3_client.upload_file(str(LOCAL_PATH), BUCKET_NAME, S3_KEY)
    except ClientError as e:
        logging.error(f"Upload failed: {e}")
        return False

    logging.info("Upload OK.")
    return True


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    upload_latest_to_s3()


if __name__ == "__main__":
    main()