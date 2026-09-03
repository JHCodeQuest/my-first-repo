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

from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from dotenv import load_dotenv

load_dotenv()

RESOURCE_GROUP = "security-lab-rg"
LOCATION = "eastus"
STORAGE_ACCOUNT_NAME = "securitylabstorage001"


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
