---
title: IAM Least Privilege
order: 1
summary: Why broad IAM permissions are the #1 cause of AWS breaches, and how to scope them down.
---

## The problem

Most AWS security incidents trace back to an IAM identity (user, role, or
access key) that had far more permission than it needed. A leaked key for a
user with `AdministratorAccess` is a full account takeover; the same leak on
a role scoped to `s3:GetObject` on one bucket is a non-event.

## Core ideas

- **Start from zero.** Grant only the specific actions and resources a
  workload needs, not a whole service (`s3:*`) or `*` resources.
- **Prefer roles over long-lived access keys.** Roles issue short-lived
  credentials that auto-expire; a leaked static key doesn't.
- **Use IAM Access Analyzer** to find policies that grant access to
  resources outside your account, and unused permissions you can remove.
- **Separate humans from workloads.** People should assume roles via SSO,
  not hold permanent access keys at all.

## Try it yourself (safe, no cloud account needed)

Read the policy below and identify what's wrong with it before checking the
answer.

```json
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

<details>
<summary>Answer</summary>

This grants every S3 action (including `DeleteBucket`, `PutBucketPolicy`,
`PutObjectAcl`) on every bucket in the account. A minimal version for "read
objects from one bucket" would be:

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-specific-bucket/*"
}
```
</details>

## Next lab

When you're ready to practice this against a real (isolated) AWS sandbox
account, see `infra/aws/README.md` in this repo.
