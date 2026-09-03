---
title: Public Storage Accounts
order: 2
summary: Azure's equivalent to the "open S3 bucket" mistake — public blob containers.
---

## The problem

Azure Storage accounts and their blob containers can independently be set
to allow anonymous public read access. It's Azure's equivalent of an open
S3 bucket, and just as common a cause of data exposure.

## Core ideas

- **"Allow Blob public access" is an account-level switch.** Turn it off
  at the storage account unless you specifically need public content
  (e.g. hosting static website assets).
- **Container-level access** (Private / Blob / Container) is a second
  layer — both the account switch and the container setting must allow
  public access for data to actually be exposed.
- **Shared Access Signatures (SAS)** are the safer way to give time-limited,
  scoped access to specific blobs instead of making a container public.
- **Microsoft Defender for Cloud** flags storage accounts configured for
  public access as a security recommendation.

## Try it yourself (safe, no cloud account needed)

A storage account has "Allow Blob public access" set to **Enabled** at the
account level, and one container inside it is set to **Private**. Is that
container publicly readable?

<details>
<summary>Answer</summary>

No — both layers must allow it. The account-level switch only permits
public access to be configured; the container's own setting (Private)
still blocks it. But any *other* container in that account set to "Blob"
or "Container" access would be exposed, so the account-level switch being
on is still a risk worth flagging.
</details>

## Next lab

When you're ready to practice this against a real (isolated) Azure sandbox
subscription, see `infra/azure/README.md` in this repo.
