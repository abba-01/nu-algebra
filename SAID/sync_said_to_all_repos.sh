#!/bin/bash
# SAID Sync Script
# Syncs the master SAID directory from abba repo to all other repositories

# Note: Not using 'set -e' to allow script to continue even if individual operations fail

MASTER_REPO="/run/media/root/OP01/got/abba"
REPOS_DIR="/run/media/root/OP01/got"
SAID_SOURCE="$MASTER_REPO/SAID"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== SAID Sync Script ===${NC}"
echo "Master source: $SAID_SOURCE"
echo ""

if [ ! -d "$SAID_SOURCE" ]; then
    echo -e "${RED}Error: Master SAID directory not found at $SAID_SOURCE${NC}"
    exit 1
fi

# Counter
UPDATED=0
SKIPPED=0

# Iterate through all repos using absolute paths
for repo_path in "$REPOS_DIR"/*/ ; do
    # Get just the repo name
    repo_name=$(basename "$repo_path")

    # Skip abba (master) and non-git directories
    if [ "$repo_name" == "abba" ] || [ ! -d "$repo_path/.git" ]; then
        continue
    fi

    echo -e "${YELLOW}Processing: $repo_name${NC}"

    # Copy SAID directory using absolute paths
    cp -r "$SAID_SOURCE" "$repo_path/"

    # Check if there are changes (use -C to run git in that directory)
    if git -C "$repo_path" diff --quiet SAID/; then
        echo -e "${GREEN}✓ No changes needed${NC}"
        ((SKIPPED++))
    else
        # Commit changes (use -C to run git in that directory)
        git -C "$repo_path" add SAID/
        git -C "$repo_path" commit -m "Update SAID framework from master

Synced from: https://github.com/abba-01/abba/tree/main/SAID

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

        echo -e "${GREEN}✓ Updated and committed${NC}"
        ((UPDATED++))
    fi

    echo ""
done

echo -e "${GREEN}=== Sync Complete ===${NC}"
echo "Updated: $UPDATED repositories"
echo "Skipped (no changes): $SKIPPED repositories"
echo ""
echo "To push all changes, run:"
echo "  cd /run/media/root/OP01/got"
echo "  for repo in */; do (cd \$repo && git push); done"
