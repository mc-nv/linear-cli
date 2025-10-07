#!/bin/bash
# Example usage script for Linear CLI
# This demonstrates various ways to use the linear-cli tool

echo "Linear CLI - Example Usage Script"
echo "=================================="
echo ""

# Setup (you would normally do this once in your shell profile)
# export LINEAR_CLI_TOKEN="lin_api_xxxxxxxxxxxxx"
# export LINEAR_CLI_TEAM_ID="your-team-id"

# Check if token is set
if [ -z "$LINEAR_CLI_TOKEN" ]; then
    echo "ERROR: LINEAR_CLI_TOKEN is not set!"
    echo "Please set it with: export LINEAR_CLI_TOKEN='your-token-here'"
    exit 1
fi

echo "✓ Token is configured"
echo ""

# Example 1: Create a simple issue
echo "Example 1: Creating a simple issue"
echo "-----------------------------------"
linear-cli create --title "Example: Simple task"
echo ""

# Example 2: Create a bug report using template
echo "Example 2: Creating a bug report"
echo "--------------------------------"
linear-cli create \
    --title "Login fails on Safari" \
    --description "Users report they cannot log in using Safari browser" \
    --template bug \
    --priority 1
echo ""

# Example 3: Create a feature request
echo "Example 3: Creating a feature request"
echo "-------------------------------------"
linear-cli create \
    --title "Add export to CSV functionality" \
    --template feature \
    --priority 3
echo ""

# Example 4: List recent issues
echo "Example 4: Listing recent issues"
echo "--------------------------------"
linear-cli list --limit 5
echo ""

# Example 5: Search for issues
echo "Example 5: Searching for issues"
echo "--------------------------------"
linear-cli search "bug" --limit 5
echo ""

# Example 6: Show issue details (you'll need to replace ABC-123 with a real issue ID)
echo "Example 6: Showing issue details"
echo "--------------------------------"
echo "(Replace ABC-123 with a real issue ID from your list above)"
# linear-cli show ABC-123
echo ""

# Example 7: Get issues assigned to you
echo "Example 7: Getting your assigned issues"
echo "---------------------------------------"
linear-cli my-issues --limit 5
echo ""

# Example 8: Get issues in JSON format
echo "Example 8: Getting your issues in JSON format"
echo "---------------------------------------------"
linear-cli my-issues --json --limit 3
echo ""

# Example 9: Using with logging
echo "Example 9: Creating an issue with logging enabled"
echo "------------------------------------------------"
linear-cli --log --verbose create --title "Example: Task with logging"
echo ""
echo "Check linear-cli.log for detailed logs"
echo ""

# Example 10: Using custom log file
echo "Example 10: Using custom log file"
echo "---------------------------------"
linear-cli --log --log-file /tmp/my-linear.log create --title "Example: Custom log location"
echo "Check /tmp/my-linear.log for logs"
echo ""

echo "Examples completed!"
echo ""
echo "To use these examples, make sure to:"
echo "1. Set LINEAR_CLI_TOKEN environment variable"
echo "2. Optionally set LINEAR_CLI_TEAM_ID for team-specific operations"
echo "3. Replace placeholder IDs with real values from your Linear workspace"
