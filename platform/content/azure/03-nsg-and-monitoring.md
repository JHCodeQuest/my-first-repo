---
title: Network Security Groups & Monitoring
order: 3
summary: Locking down network paths and making sure you can see what happens on them.
---

## The problem

Azure Network Security Groups (NSGs) filter traffic to VMs and subnets by
IP, port, and protocol. A common mistake is leaving management ports
(RDP 3389, SSH 22) open to `Any`/`Internet` instead of a specific IP range
— the #1 way Azure VMs get brute-forced within hours of deployment.

## Core ideas

- **Never expose 22/3389 to `Any`.** Use a specific IP range (your office
  or VPN), Azure Bastion, or Just-In-Time VM access instead.
- **NSGs apply at both the subnet and NIC level** — traffic must be
  allowed by both to reach a VM, which is a common source of "why can't I
  connect" confusion but also a defense-in-depth opportunity.
- **Azure Monitor + Log Analytics** collect NSG flow logs so you can see
  what traffic was actually allowed/denied, not just what your rules say
  in theory.
- **Microsoft Sentinel** (Azure's SIEM) can alert on patterns like repeated
  failed logins or traffic from known-malicious IP ranges.

## Try it yourself (safe, no cloud account needed)

An NSG rule allows inbound TCP port 3389 from source `0.0.0.0/0`
(i.e. `Any`) to a VM. What's the fix, and what Azure feature avoids needing
this rule at all?

<details>
<summary>Answer</summary>

Fix: restrict the source to a known IP range (e.g. your office's public
IP) rather than `Any`. Better: use **Azure Bastion** or **Just-In-Time VM
access** (via Microsoft Defender for Cloud) so RDP is never exposed to the
internet at all — it's brokered through Azure instead.
</details>

## Next lab

When you're ready to practice this against a real (isolated) Azure sandbox
subscription, see `infra/azure/README.md` in this repo.
