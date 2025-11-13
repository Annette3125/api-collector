import logging
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

# real bucket name
BUCKET_NAME = "annette-etl-data"
S3_KEY = "raw/stock_data_latest.csv"  # way inside S3
LOCAL_PATH = Path("data/new/stock_data_latest.csv")


def upload_latest_to_s3() -> bool:
    """
    Uploads latest CSV (data/new/stock_data_latest.csv) to S3 bucket.
    Credentials use from `aws configure`.
    """
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
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    upload_latest_to_s3()


if __name__ == "__main__":
    main()
