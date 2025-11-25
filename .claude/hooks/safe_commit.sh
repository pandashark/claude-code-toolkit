#!/bin/bash
# Safe commit wrapper that enforces quality checks
# This replaces direct git commit to prevent --no-verify

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for forbidden flags
for arg in "$@"; do
    if [[ "$arg" == "--no-verify" ]] || [[ "$arg" == "-n" ]]; then
        echo -e "${RED}❌ ERROR: --no-verify is not allowed${NC}"
        echo "All commits must pass quality checks."
        echo "Fix any issues and commit without --no-verify"
        exit 1
    fi
done

echo -e "${GREEN}🔍 Running quality checks before commit...${NC}"

# Run pre-commit hook explicitly
if [ -f .git/hooks/pre-commit ]; then
    .git/hooks/pre-commit
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Quality checks failed${NC}"
        exit 1
    fi
fi

# If all checks pass, perform the commit
echo -e "${GREEN}✅ Quality checks passed, committing...${NC}"
git commit "$@"