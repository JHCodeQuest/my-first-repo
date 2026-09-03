"""Delete the entire lab resource group created by provision.py."""
import os
import sys

from azure.core.exceptions import ResourceNotFoundError
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from dotenv import load_dotenv

load_dotenv()

RESOURCE_GROUP = "security-lab-rg"


def main():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = ClientSecretCredential(
        tenant_id=os.environ["AZURE_TENANT_ID"],
        client_id=os.environ["AZURE_CLIENT_ID"],
        client_secret=os.environ["AZURE_CLIENT_SECRET"],
    )

    resource_client = ResourceManagementClient(credential, subscription_id)
    try:
        rg = resource_client.resource_groups.get(RESOURCE_GROUP)
    except ResourceNotFoundError:
        print(f"Nothing to do: resource group '{RESOURCE_GROUP}' does not exist.")
        return

    if rg.tags is None or rg.tags.get("purpose") != "security-lab":
        sys.exit(
            f"Refusing to delete '{RESOURCE_GROUP}': missing the "
            "'purpose=security-lab' tag this script expects."
        )

    poller = resource_client.resource_groups.begin_delete(RESOURCE_GROUP)
    poller.result()
    print(f"Deleted resource group: {RESOURCE_GROUP}")


if __name__ == "__main__":
    main()
