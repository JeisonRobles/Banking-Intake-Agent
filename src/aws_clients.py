# src/aws_clients.py
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
AWS_PROFILE = os.getenv("AWS_PROFILE")

def _session() -> boto3.Session:
    """
    Creates a boto3 Session using an optional profile name.
    Region is always pinned to AWS_REGION.
    """
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)

def ddb_table():
    """
    Returns a DynamoDB Table resource.

    Env vars:
      - DDB_TABLE_NAME (recommended) or DDB_TABLE
      - AWS_REGION / AWS_DEFAULT_REGION
      - AWS_PROFILE (optional)
    """
    table_name = os.getenv("DDB_TABLE_NAME") or os.getenv("DDB_TABLE") or "banking-tickets"

    # Build the DynamoDB resource explicitly with region
    dynamodb = _session().resource("dynamodb", region_name=AWS_REGION)

    # Optional debug
    # print(f"Using region={AWS_REGION}, table={table_name}, profile={AWS_PROFILE or 'default'}")

    return dynamodb.Table(table_name)