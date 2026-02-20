import os
import mimetypes
import uuid
from datetime import datetime, timezone

from aws_clients import ddb_table

def upload_image(id: str,
                 ticket_id:int,
                 first_name:str,
                 last_name:str,
                 contact_method:str,
                 contact:str,
                 interested_product:str) -> dict:

    table = ddb_table()

    #Creation Footprint
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat().replace("+00:00", "Z")

    # Save metadata to DynamoDB
    item = {
        "id": id,
        "ticket_id": ticket_id,
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
    parser.add_argument("--ticket_id", required=True)
    parser.add_argument("--first_name", required=True)
    parser.add_argument("--last_name", required=True)
    parser.add_argument("--contact_method", required=True)
    parser.add_argument("--contact", required=True)
    parser.add_argument("--interested_product", required=True)
    args = parser.parse_args()
    result = upload_image(args.id, args.ticket_id, args.first_name, args.last_name, args.contact_method, args.contact, args.interested_product)
    print("Ticket successfully created...")
    print(result)
    