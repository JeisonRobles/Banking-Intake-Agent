import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_PROFILE = os.getenv("AWS_PROFILE")
AWS_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"

def ddb_table():
    table_name = os.getenv("DDB_TABLE_NAME") or "banking-tickets"

    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION) if AWS_PROFILE else boto3.Session(region_name=AWS_REGION)
    dynamodb = session.resource("dynamodb")
    return dynamodb.Table(table_name)