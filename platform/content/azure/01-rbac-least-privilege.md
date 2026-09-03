---
title: Azure RBAC Least Privilege
order: 1
summary: Azure's version of "don't grant more than you need" — roles, scopes, and the Owner trap.
---

## The problem

Azure RBAC assigns roles at a **scope** (management group, subscription,
resource group, or single resource). A common mistake is assigning
`Owner` or `Contributor` at the subscription level to a person or service
principal that only ever touches one resource group.

## Core ideas

- **Scope down, not up.** Assign roles at the narrowest scope that covers
  the actual job — a single resource group, not the whole subscription.
- **Use built-in roles before custom ones.** Azure has hundreds of scoped
  built-in roles (e.g. `Storage Blob Data Reader`) that are narrower than
  `Contributor`.
- **Service principals should hold roles, not `Owner`.** `Owner` includes
  the ability to grant *other* people access — rarely what an automated
  pipeline needs.
- **Privileged Identity Management (PIM)** lets you make privileged roles
  *eligible* rather than permanently active — a user activates the role
  only when needed, for a limited time, often with approval required.

## Try it yourself (safe, no cloud account needed)

A CI/CD pipeline needs to deploy container images to one Azure Container
Registry. Which is the better role assignment?

- A) `Owner` on the subscription
- B) `AcrPush` on the specific registry resource

<details>
<summary>Answer</summary>

B. `AcrPush` grants exactly the permission needed (push images to that
registry) at the narrowest possible scope. Option A would let a leaked
pipeline credential modify or delete anything in the entire subscription.
</details>

## Next lab

When you're ready to practice this against a real (isolated) Azure sandbox
subscription, see `infra/azure/README.md` in this repo.
