# .ai Directory

This directory contains AI collaboration instructions and policies.

## Purpose

Provides a centralized location for AI tools to discover collaboration guidelines before interacting with this repository.

## Contents

- `instructions.md` - Primary AI instructions (references guardrails)
- Referenced policy: `../edm.guardrails_live.json` (source of truth)

## Convention

The `.ai/` directory is an emerging standard for repository-level AI instructions. Tools that support this convention will automatically check this directory before performing tasks.

## Distribution

This directory is:
- ✅ Tracked in git
- ✅ Auto-synced to dependent repositories
- ❌ Excluded from source distributions (via .gitignore)
- ❌ Not compiled into packages

## Sync Source

This repository (`abba-01/said`) is the master source. Changes here automatically propagate to:
- abba-01/nualgebra
- abba-01/nualgebra_psychology
- abba-01/nualgebra_anthropology

## Maintenance

Update guardrails in `edm.guardrails_live.json` (parent directory).
AI instructions in `.ai/instructions.md` reference the live policy.
