#!/bin/bash
# Linear CLI Environment Configuration Template
# Copy this to your shell profile (~/.bashrc, ~/.zshrc, etc.) and fill in your values

# Required: Linear API Token
# Get your token from: https://linear.app/settings/api
export LINEAR_CLI_TOKEN="lin_api_xxxxxxxxxxxxx"

# Optional: Default Team ID
# Find your team ID in the Linear URL or via the API
# Example: When viewing team issues, URL might be linear.app/team/TEAM-abc123
# export LINEAR_CLI_TEAM_ID="12345678-1234-1234-1234-123456789abc"

# Optional: Default Template
# Options: default, bug, feature
# export LINEAR_CLI_TEMPLATE="default"

# Optional: Custom Log File Path
# Default is: linear-cli.log
# export LINEAR_CLI_LOG_FILE="$HOME/.linear-cli.log"

# Optional: Add linear-cli to your PATH if installed in a custom location
# export PATH="$PATH:/path/to/linear-cli/bin"

echo "Linear CLI environment configured ✓"
