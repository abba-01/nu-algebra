# SAID Directory
**Scientific Academic Integrity Disclosure**

This directory contains transparency and integrity documentation for this research project.

## Quick Links

📄 **[What is SAID?](Scientific_Academic_Integrity_Disclosure.md)** - Full documentation of the SAID framework

📋 **[Guardrails Policy](guardrails_v1_2025.json)** - AI collaboration constraints (v1.2)

---

## TL;DR

**SAID** = **S**cientific **A**cademic **I**ntegrity **D**isclosure

This framework documents how AI was used in this research, with explicit guardrails ensuring:
- No fabrication or speculation
- Reproducible, deterministic outputs
- Verifiable sources and provenance
- Transparent methodology

**Why this matters**: Trust, reproducibility, and responsible AI use in science.

---

## Master Repository & Auto-Sync

This SAID directory is **automatically synchronized** from the master repository:

🏠 **Master**: [abba-01/abba/SAID](https://github.com/abba-01/abba/tree/main/SAID)

**How it works**:
- ✅ Changes to SAID in abba repo trigger automatic sync to all repositories
- ✅ Git post-commit hook runs `sync_said_to_all_repos.sh`
- ✅ All repos stay synchronized with a single source of truth

**Manual sync** (if needed):
```bash
cd /run/media/root/OP01/got/abba
./SAID/sync_said_to_all_repos.sh
```

---

For complete details, see [Scientific_Academic_Integrity_Disclosure.md](Scientific_Academic_Integrity_Disclosure.md)
