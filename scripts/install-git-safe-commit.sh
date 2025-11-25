#!/bin/bash
# Install git-safe-commit globally
# This script installs the git safe-commit wrapper to enforce quality checks

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "📦 Installing git-safe-commit..."
echo ""

# Determine installation directory
INSTALL_DIR="${HOME}/.local/bin"

# Create directory if it doesn't exist
if [ ! -d "$INSTALL_DIR" ]; then
    echo "→ Creating ${INSTALL_DIR}..."
    mkdir -p "$INSTALL_DIR"
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_SCRIPT="${SCRIPT_DIR}/../.claude/hooks/safe_commit.sh"

# Check if source exists
if [ ! -f "$SOURCE_SCRIPT" ]; then
    echo -e "${RED}❌ Error: Source script not found at ${SOURCE_SCRIPT}${NC}"
    echo "Make sure you're running this from the Claude Code Toolkit directory."
    exit 1
fi

# Copy script
echo "→ Installing to ${INSTALL_DIR}/git-safe-commit..."
cp "$SOURCE_SCRIPT" "${INSTALL_DIR}/git-safe-commit"
chmod +x "${INSTALL_DIR}/git-safe-commit"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":${HOME}/.local/bin:"* ]]; then
    echo ""
    echo -e "${YELLOW}⚠️  Warning: ${HOME}/.local/bin is not in your PATH${NC}"
    echo ""
    echo "Add this to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
    echo ""
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Then restart your shell or run: source ~/.bashrc"
    echo ""
else
    echo -e "${GREEN}✅ ${HOME}/.local/bin is already in your PATH${NC}"
fi

# Verify installation
if command -v git-safe-commit >/dev/null 2>&1; then
    echo ""
    echo -e "${GREEN}✅ Installation complete!${NC}"
    echo ""
    echo "Usage:"
    echo "    git safe-commit -m \"feat: your commit message\""
    echo ""
    echo "The wrapper enforces:"
    echo "  - Blocks --no-verify flag"
    echo "  - Runs pre-commit hooks"
    echo "  - Ensures quality checks pass"
else
    echo ""
    echo -e "${YELLOW}⚠️  Installed but not yet in PATH${NC}"
    echo "Restart your shell or add ${HOME}/.local/bin to PATH"
fi
