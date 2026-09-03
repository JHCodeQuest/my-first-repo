# My First Repo

Learning DevOps with Git

[![roadmap.sh](https://roadmap.sh/card/tall/69cfeb706ead7173a7c0687b?variant=dark&roadmaps=git-github)](https://roadmap.sh)

## Security Learning Platform

A small Flask web app for learning cloud security concepts, no CLI
required to use it day-to-day. AWS and Azure are two completely
independent tracks — separate content, separate optional lab
infrastructure, separate credentials — so they never compete for the same
space.

```
platform/   Flask app: dashboard, lessons, progress tracking
infra/aws/  Guarded scripts to spin up a real, isolated AWS lab (optional)
infra/azure/ Guarded scripts to spin up a real, isolated Azure lab (optional)
```

### Run the platform

```bash
cd platform
pip install -r requirements.txt
python3 app.py
```

Then open http://127.0.0.1:5000 in a browser. Progress is stored locally
in `platform/progress.db` (ignored by git).

### Optional: real cloud labs

The lessons are fully self-contained and safe on their own — no cloud
account needed. If you want to practice against a real, isolated sandbox
account later, see `infra/aws/README.md` and `infra/azure/README.md`.
Those scripts:

- Never run automatically or from the web app.
- Refuse to execute unless you explicitly set `CONFIRM_LAB=yes`.
- Only ever create resources with public access disabled.
- Come with a matching `destroy.py` to tear everything down.

Fill in your own credentials in a local `.env` file (copy
`.env.example` — see below) before using them. Never commit `.env`.

## .env.example

`.env.example` lists the names of tokens/credentials this repo's tooling
can use (AWS, Azure, GitHub, security scanners, etc.) with no values
filled in. Copy it to `.env` and fill in your own — `.env` is gitignored.
