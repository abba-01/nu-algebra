#!/bin/bash
# AI Guardrails Checkpoint - "Bouncer" at repo entrance
# Validates AI interactions comply with guardrails policy

set -e

GUARDRAILS_FILE="../edm.guardrails_live.json"
CHECKPOINT_LOG=".ai/.checkpoint.log"

echo "════════════════════════════════════════════════"
echo "   🚦 AI GUARDRAILS CHECKPOINT"
echo "════════════════════════════════════════════════"
echo ""

# Check if guardrails file exists
if [ ! -f "$GUARDRAILS_FILE" ]; then
    echo "❌ CHECKPOINT FAILED: Guardrails file not found"
    echo "   Expected: $GUARDRAILS_FILE"
    exit 1
fi

# Verify guardrails version
VERSION=$(grep -o '"version": "[^"]*"' "$GUARDRAILS_FILE" | head -1 | cut -d'"' -f4)
echo "📋 Guardrails Version: $VERSION"

# Extract key constraints
MODE=$(grep -o '"name": "[^"]*"' "$GUARDRAILS_FILE" | head -1 | cut -d'"' -f4)
echo "🔒 Policy Mode: $MODE"

# Check for required sections
REQUIRED_SECTIONS=(
    "validation_framework"
    "interaction_policies"
    "manuscript_production_policy"
    "truth_integrity_clause"
)

echo ""
echo "🔍 Validating guardrails structure..."
for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -q "\"$section\"" "$GUARDRAILS_FILE"; then
        echo "   ✅ $section"
    else
        echo "   ❌ Missing: $section"
        exit 1
    fi
done

# Log checkpoint
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "$TIMESTAMP - Checkpoint passed - Version: $VERSION" >> "$CHECKPOINT_LOG"

echo ""
echo "════════════════════════════════════════════════"
echo "   ✅ CHECKPOINT PASSED"
echo "════════════════════════════════════════════════"
echo ""
echo "AI collaboration authorized with constraints:"
echo "• Scaffolding only (no full manuscripts)"
echo "• Verifiable artifacts required"
echo "• Simple language, short sentences"
echo "• No fabrication or speculation"
echo ""
echo "Proceed with task execution under guardrails compliance."
echo ""
