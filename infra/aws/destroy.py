"""Tear down a lab bucket created by provision.py.

Usage: python3 destroy.py security-lab-1234567890
"""
import os
import sys

import boto3
from dotenv import load_dotenv

load_dotenv()


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 destroy.py <bucket-name>")

    bucket_name = sys.argv[1]
    if not bucket_name.startswith("security-lab-"):
        sys.exit("Refusing to delete a bucket not created by this lab (must start with 'security-lab-').")

    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    s3 = boto3.client("s3", region_name=region)

    objects = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
    for obj in objects:
        s3.delete_object(Bucket=bucket_name, Key=obj["Key"])

    s3.delete_bucket(Bucket=bucket_name)
    print(f"Deleted bucket: {bucket_name}")


if __name__ == "__main__":
    main()
