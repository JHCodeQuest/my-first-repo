"""Create a resource group + storage account for the Azure security lab.

Safety by design:
- Refuses to run unless CONFIRM_LAB=yes is set, so it never fires by accident.
- Creates exactly one resource group, tagged "purpose=security-lab".
- Leaves "Allow Blob public access" disabled — nothing this script creates
  is internet-exposed.
- Pair with destroy.py to tear everything down when you're done.
"""
import os
import sys
import uuid

from azure.core.exceptions import ResourceNotFoundError
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from dotenv import load_dotenv

load_dotenv()

RESOURCE_GROUP = "security-lab-rg"
LOCATION = "eastus"
# Azure storage account names are globally unique across all of Azure, so a
# fixed name would collide with anyone else running this repo. Suffix it.
STORAGE_ACCOUNT_NAME = f"seclab{uuid.uuid4().hex[:16]}"


def get_credential():
    return ClientSecretCredential(
        tenant_id=os.environ["AZURE_TENANT_ID"],
        client_id=os.environ["AZURE_CLIENT_ID"],
        client_secret=os.environ["AZURE_CLIENT_SECRET"],
    )


def main():
    if os.environ.get("CONFIRM_LAB") != "yes":
        sys.exit(
            "Refusing to run: set CONFIRM_LAB=yes to confirm you want to "
            "create real Azure resources in this subscription."
        )

    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = get_credential()

    resource_client = ResourceManagementClient(credential, subscription_id)

    # Never adopt a resource group we didn't create. If one already exists
    # under this name, claiming it would also tag it "purpose=security-lab",
    # which is exactly what destroy.py uses to decide it is safe to delete.
    # Adopting a pre-existing group would therefore arm destroy.py to wipe
    # resources that are not ours.
    try:
        existing = resource_client.resource_groups.get(RESOURCE_GROUP)
    except ResourceNotFoundError:
        existing = None

    if existing is not None:
        tags = existing.tags or {}
        if tags.get("purpose") != "security-lab":
            sys.exit(
                f"Refusing to run: resource group '{RESOURCE_GROUP}' already "
                "exists and was not created by this lab. Delete it yourself "
                "or change RESOURCE_GROUP in this script before continuing."
            )
        print(f"Reusing existing lab resource group '{RESOURCE_GROUP}'.")
    else:
        resource_client.resource_groups.create_or_update(
            RESOURCE_GROUP,
            {"location": LOCATION, "tags": {"purpose": "security-lab"}},
        )

    storage_client = StorageManagementClient(credential, subscription_id)
    poller = storage_client.storage_accounts.begin_create(
        RESOURCE_GROUP,
        STORAGE_ACCOUNT_NAME,
        {
            "sku": {"name": "Standard_LRS"},
            "kind": "StorageV2",
            "location": LOCATION,
            "allow_blob_public_access": False,
            "tags": {"purpose": "security-lab"},
        },
    )
    poller.result()

    print(f"Created resource group '{RESOURCE_GROUP}' with storage account "
          f"'{STORAGE_ACCOUNT_NAME}' (public blob access: disabled)")
    print("Run destroy.py when you're done.")


if __name__ == "__main__":
    main()
