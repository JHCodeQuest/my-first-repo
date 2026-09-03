"""Create a single, tagged, non-public S3 bucket for the AWS security lab.

Safety by design:
- Refuses to run unless CONFIRM_LAB=yes is set, so it never fires by accident.
- Creates exactly one resource type (S3 bucket), tagged "purpose=security-lab".
- Leaves Block Public Access ON — nothing this script creates is internet-exposed.
- Pair with destroy.py to tear everything down when you're done.
"""
import os
import sys
import time

import boto3
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = f"security-lab-{int(time.time())}"


def main():
    if os.environ.get("CONFIRM_LAB") != "yes":
        sys.exit(
            "Refusing to run: set CONFIRM_LAB=yes to confirm you want to "
            "create real AWS resources in this account."
        )

    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    s3 = boto3.client("s3", region_name=region)

    create_args = {"Bucket": BUCKET_NAME}
    if region != "us-east-1":
        create_args["CreateBucketConfiguration"] = {"LocationConstraint": region}
    s3.create_bucket(**create_args)

    s3.put_public_access_block(
        Bucket=BUCKET_NAME,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )

    s3.put_bucket_tagging(
        Bucket=BUCKET_NAME,
        Tagging={"TagSet": [{"Key": "purpose", "Value": "security-lab"}]},
    )

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="placeholder.txt",
        Body=b"This is a lab placeholder object, not real data.",
    )

    print(f"Created bucket: {BUCKET_NAME} (Block Public Access: ON)")
    print("Run destroy.py with this bucket name when you're done.")


if __name__ == "__main__":
    main()
