# Automatic SAID Synchronization

This document explains how the automatic SAID sync system works.

---

## Overview

The SAID framework uses **git post-commit hooks** to automatically synchronize changes from the master repository (abba) to all other repositories.

---

## How It Works

### 1. Master Repository Setup

**Location**: `/run/media/root/OP01/got/abba/`

**Components**:
```
abba/
├── SAID/
│   ├── README.md
│   ├── Scientific_Academic_Integrity_Disclosure.md
│   ├── guardrails_v1_2025.json
│   └── sync_said_to_all_repos.sh          ← Sync script
└── .git/hooks/
    └── post-commit                         ← Automatic trigger
```

### 2. Trigger Mechanism

When you commit changes to the **abba** repository:

1. **Git post-commit hook** executes automatically
2. Hook checks if SAID directory was modified in the commit
3. If SAID changed → runs `sync_said_to_all_repos.sh`
4. Sync script copies SAID to all other repos and commits changes

### 3. Sync Process

```bash
# Automatic flow on commit to abba/SAID/
git commit -m "Update SAID"
  ↓
post-commit hook detects SAID/ change
  ↓
sync_said_to_all_repos.sh runs
  ↓
Copies SAID/ to all repos
  ↓
Commits changes to each repo
  ↓
Reports: "Updated X repositories"
```

---

## Technical Details

### Post-Commit Hook

**File**: `abba/.git/hooks/post-commit`

```bash
#!/bin/bash
# Check if SAID directory was modified
SAID_CHANGED=$(git diff-tree --no-commit-id --name-only -r HEAD | grep "^SAID/")

if [ -n "$SAID_CHANGED" ]; then
    # Run sync script
    bash "$REPO_ROOT/SAID/sync_said_to_all_repos.sh"
fi
```

### Sync Script

**File**: `SAID/sync_said_to_all_repos.sh`

- Iterates through all repositories in `/run/media/root/OP01/got/`
- Copies SAID from abba to each repo
- Commits changes if detected (skips if no changes)
- Reports success/skip status

---

## Usage Examples

### Automatic Sync (Recommended)

```bash
# Edit SAID files in master repo
cd /run/media/root/OP01/got/abba
vim SAID/guardrails_v1_2025.json

# Commit changes - automatic sync happens!
git add SAID/
git commit -m "Update guardrails policy"
# → Hook automatically syncs to all repos
```

### Manual Sync (Fallback)

```bash
# If hook doesn't work or manual sync needed
cd /run/media/root/OP01/got/abba
./SAID/sync_said_to_all_repos.sh
```

---

## Verification

Check if auto-sync is working:

```bash
# 1. Verify hook exists and is executable
ls -la /run/media/root/OP01/got/abba/.git/hooks/post-commit

# 2. Check for CRLF issues (should say "ASCII text executable")
file /run/media/root/OP01/got/abba/.git/hooks/post-commit

# 3. Test manually
cd /run/media/root/OP01/got/abba
.git/hooks/post-commit
```

---

## Troubleshooting

### Hook Not Executing

**Problem**: Post-commit hook doesn't run after commit

**Solutions**:
```bash
# 1. Check if executable
chmod +x .git/hooks/post-commit

# 2. Fix line endings (CRLF → LF)
sed -i 's/\r$//' .git/hooks/post-commit
sed -i 's/\r$//' SAID/sync_said_to_all_repos.sh

# 3. Verify no syntax errors
bash -n .git/hooks/post-commit
```

### Sync Script Fails

**Problem**: Sync script encounters errors

**Check**:
```bash
# 1. Ensure script is executable
chmod +x SAID/sync_said_to_all_repos.sh

# 2. Test manually
./SAID/sync_said_to_all_repos.sh

# 3. Check repository paths
ls /run/media/root/OP01/got/
```

---

## Repository List

Currently syncing to:
- ✅ abba (master)
- ✅ aiwared.org
- ✅ autonomoustheory.org
- ✅ count2infinity
- ✅ Eric-D-Martin
- ✅ nualgebra
- ✅ nu_anthropology
- ✅ nua_psychology
- ✅ observer.MetaModalPlatform.org
- ✅ theories
- ✅ uha

---

## Pushing Updates

After automatic sync, **push all repositories**:

```bash
# Push all repos to GitHub
cd /run/media/root/OP01/got
for repo in */; do
  (cd "$repo" && git push)
done
```

Or push individually:
```bash
cd /run/media/root/OP01/got/nualgebra
git push
```

---

## Maintenance

### Adding New Repository

1. Clone/create new repo in `/run/media/root/OP01/got/`
2. Next SAID commit in abba will auto-sync to new repo
3. Verify sync: `ls /path/to/new-repo/SAID/`

### Removing Repository

1. Delete repo from `/run/media/root/OP01/got/`
2. Sync script will automatically skip missing repos

### Updating Hook Logic

1. Edit `abba/.git/hooks/post-commit`
2. Test: `bash -n .git/hooks/post-commit`
3. Commit change to test (does NOT sync hook itself)

---

## Security Notes

- ✅ Hook runs in local environment only
- ✅ No remote execution or network calls
- ✅ All operations are file-based git commits
- ✅ Hook source is version-controlled (documented, not in repo)

---

**Last Updated**: 2025-10-07
**Status**: Active and tested
**Version**: 1.0
