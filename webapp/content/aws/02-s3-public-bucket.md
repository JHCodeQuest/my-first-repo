---
title: Public S3 Buckets
order: 2
summary: How buckets end up world-readable, and the settings that stop it.
---

## The problem

A public S3 bucket is one of the most common real-world breach causes —
company data, backups, or even source code left readable by anyone with the
URL. It usually happens through a bucket policy or ACL that grants access to
`*` (everyone), often copy-pasted from a tutorial without adjusting the
`Principal`.

## Core ideas

- **S3 Block Public Access** is an account- and bucket-level switch that
  overrides any policy trying to make the bucket public. Leave it ON unless
  you have a specific, reviewed reason to host public content.
- **Bucket policies vs ACLs**: prefer bucket policies (clearer, auditable)
  over legacy ACLs.
- **IAM Access Analyzer for S3** flags buckets that are public or shared
  outside the account.
- **CloudTrail data events** let you see who actually accessed objects, so
  you can detect exposure even before you notice the misconfiguration.

## Try it yourself (safe, no cloud account needed)

Spot the issue in this bucket policy:

```json
{
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::company-backups/*"
}
```

<details>
<summary>Answer</summary>

`"Principal": "*"` means *anyone on the internet*, not just your account or
application. Unless this bucket is meant to serve public static content
(like a website), this should instead grant access to a specific role or
account, e.g. `"Principal": {"AWS": "arn:aws:iam::123456789012:role/backup-reader"}`.
</details>

## Next lab

When you're ready to practice this against a real (isolated) AWS sandbox
account, see `infra/aws/README.md` in this repo.
