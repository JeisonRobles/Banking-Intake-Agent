import os
from datetime import datetime, timezone

import boto3
from dotenv import load_dotenv

load_dotenv()

from tools.aws_clients import ddb_table


def create_item(
    id: str,
    ticket_id: int,
    first_name: str,
    last_name: str,
    contact_method: str,
    contact: str,
    interested_product: str,
) -> dict:

    table = ddb_table()

    # Creation footprint (UTC)
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Save metadata to DynamoDB
    item = {
        "id": str(id),
        "ticket_id": int(ticket_id),  # IMPORTANT: Dynamo sort key is Number
        "first_name": first_name,
        "last_name": last_name,
        "contact_method": contact_method,
        "contact": contact,
        "interested_product": interested_product,
        "solicitation_at": timestamp,
    }

    table.put_item(Item=item)
    return item


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--id", required=True)
    parser.add_argument("--ticket_id", required=True, type=int)  # FIX: parse as int
    parser.add_argument("--first_name", required=True)
    parser.add_argument("--last_name", required=True)
    parser.add_argument("--contact_method", required=True)
    parser.add_argument("--contact", required=True)
    parser.add_argument("--interested_product", required=True)

    args = parser.parse_args()

    result = create_item(
        id=args.id,
        ticket_id=args.ticket_id,
        first_name=args.first_name,
        last_name=args.last_name,
        contact_method=args.contact_method,
        contact=args.contact,
        interested_product=args.interested_product,
    )

    print("Ticket successfully created...")
    print(result)