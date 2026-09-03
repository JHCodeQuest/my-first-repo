# Azure lab sandbox

This is the Azure-specific lab track. It is completely independent from
the AWS track in `infra/aws/` — different subscription, different
credentials, different scripts. Nothing here runs automatically or is
wired into the web app.

## Before you touch this

1. **Use a dedicated Azure subscription for labs** — an
   [Azure free account](https://azure.microsoft.com/free/) or a separate
   subscription under your tenant, not your main one.
2. **Enable MFA** on the account you'll use to sign in.
3. **Set a budget with an alert** (Cost Management + Billing → Budgets) at
   a low threshold so you're notified if something runs away.
4. **Create an app registration / service principal for this script**
   scoped to just the lab resource group (see "Setup" below) — never use
   an account with subscription-level `Owner`.

## Setup

1. Copy `.env.example` (repo root) to `.env` and fill in:
   ```
   AZURE_CLIENT_ID=...
   AZURE_CLIENT_SECRET=...
   AZURE_TENANT_ID=...
   AZURE_SUBSCRIPTION_ID=...
   ```
2. Install dependencies:
   `pip install azure-identity azure-mgmt-resource azure-mgmt-storage python-dotenv`
3. Review `provision.py` before running it — know exactly what it creates.
4. Run it: `python3 provision.py`
   - It refuses to run unless you set `CONFIRM_LAB=yes` first.
5. When you're done experimenting, **always run** `python3 destroy.py` to
   delete the whole lab resource group and avoid ongoing charges.

## What it creates

One resource group (`security-lab-rg`) containing a single Storage
Account with "Allow Blob public access" left **disabled**, so you can
safely practice the storage-exposure lesson from the platform (e.g.
temporarily enabling public access yourself to see how Defender for Cloud
flags it, then disabling it again) without any real data ever being
exposed.
