"""Tear down a lab bucket created by provision.py.

Usage:
    python3 destroy.py                 # uses the bucket name provision.py saved
    python3 destroy.py <bucket-name>   # or name it explicitly
"""
import os
import sys
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()

STATE_FILE = Path(__file__).parent / ".lab-state"


def resolve_bucket_name():
    if len(sys.argv) == 2:
        return sys.argv[1]
    if len(sys.argv) > 2:
        sys.exit("Usage: python3 destroy.py [bucket-name]")
    if STATE_FILE.exists():
        name = STATE_FILE.read_text().strip()
        if name:
            return name
    sys.exit(
        "No bucket name given and no saved state found. Pass the name "
        "explicitly: python3 destroy.py <bucket-name>"
    )


def main():
    bucket_name = resolve_bucket_name()
    if not bucket_name.startswith("security-lab-"):
        sys.exit(
            "Refusing to delete a bucket not created by this lab "
            "(must start with 'security-lab-')."
        )

    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    s3 = boto3.client("s3", region_name=region)

    # Paginate: list_objects_v2 returns at most 1000 keys per call, and
    # delete_bucket fails with BucketNotEmpty if any object is left behind.
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get("Contents", []):
            s3.delete_object(Bucket=bucket_name, Key=obj["Key"])

    s3.delete_bucket(Bucket=bucket_name)
    print(f"Deleted bucket: {bucket_name}")

    if STATE_FILE.exists():
        STATE_FILE.unlink()


if __name__ == "__main__":
    main()
