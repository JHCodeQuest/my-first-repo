---
title: CloudTrail & Detection
order: 3
summary: Why "prevent everything" always fails, and how to at least see what happened.
---

## The problem

No set of preventive controls is perfect. When something does go wrong, the
question becomes: can you tell what happened, when, and by whom? Without
logging, an incident becomes a guessing game.

## Core ideas

- **CloudTrail** records every API call made in your account (who, what,
  when, from where). Enable it account-wide, in all regions, before you
  need it.
- **Send logs to a separate account** (or at least a locked-down bucket) so
  an attacker who compromises the primary account can't also delete the
  evidence.
- **GuardDuty** analyzes CloudTrail, VPC Flow Logs, and DNS logs for
  known-bad patterns (credential exfiltration, crypto-mining, port
  scanning) and alerts automatically — no rules to write yourself.
- **Budget/cost alarms** double as a security signal: a sudden spike often
  means compromised credentials being used to mine crypto or spin up
  resources.

## Try it yourself (safe, no cloud account needed)

Given this scenario: a `PutObject` call appears in CloudTrail from an IP
address you don't recognize, using access keys belonging to a CI/CD
service account that should only ever run from GitHub Actions' IP ranges.

<details>
<summary>What would you check first?</summary>

1. Was this access key meant to exist at all, or was it rotated/deleted and
   somehow still valid?
2. What other API calls did that access key make around the same time —
   was it just this one `PutObject`, or a broader pattern (e.g. also
   `ListBuckets`, `CreateUser`)?
3. Revoke/rotate the key immediately regardless — investigate from the logs
   after cutting off further access.
</details>

## Next lab

When you're ready to practice this against a real (isolated) AWS sandbox
account, see `infra/aws/README.md` in this repo.
