# AWS lab sandbox

This is the AWS-specific lab track. It is completely independent from the
Azure track in `infra/azure/` — different account, different credentials,
different scripts. Nothing here runs automatically or is wired into the
web app.

## Before you touch this

1. **Use a dedicated AWS account for labs**, not your main/personal
   account. Create one for free via [AWS Organizations](https://aws.amazon.com/organizations/)
   or a standalone free-tier account.
2. **Enable MFA on the root user**, then lock the root credentials away —
   never use root for day-to-day work.
3. **Create a Budget with an alert** (Billing → Budgets) at a low dollar
   threshold (e.g. $5) so you're emailed if something runs away.
4. **Create an IAM user or role for this script** with only the
   permissions in `lab-policy.json` (least privilege) — not
   `AdministratorAccess`.

## Setup

1. Copy `.env.example` (repo root) to `.env` and fill in:
   ```
   AWS_ACCESS_KEY_ID=...
   AWS_SECRET_ACCESS_KEY=...
   AWS_DEFAULT_REGION=us-east-1
   ```
2. Install dependencies: `pip install boto3 python-dotenv`
3. Review `provision.py` before running it — know exactly what it creates.
4. Run it: `python3 provision.py`
   - It refuses to run unless you set `CONFIRM_LAB=yes` first, so you
     can't trigger it by accident.
5. When you're done experimenting, **always run** `python3 destroy.py` to
   tear down every resource it created and avoid ongoing charges.
   - `provision.py` saves the generated bucket name to a local `.lab-state`
     file (gitignored), so `destroy.py` needs no arguments. You can also
     name the bucket explicitly: `python3 destroy.py security-lab-1234567890`.

## What it creates

A single S3 bucket with Block Public Access left ON, so you can safely
practice the IAM/S3 lessons from the platform (e.g. temporarily disabling
Block Public Access yourself to see the warning banners AWS shows you,
then re-enabling it) without any risk of real exposure — the bucket
contains no real data, only a placeholder object.
