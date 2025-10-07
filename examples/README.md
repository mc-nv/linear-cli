# Examples

This directory contains example scripts and configuration files to help you get started with Linear CLI.

## Files

### `env-template.sh`
Template for setting up environment variables. Copy the relevant exports to your shell profile:

```bash
# View the template
cat examples/env-template.sh

# Add to your shell profile
cat examples/env-template.sh >> ~/.zshrc
# Then edit ~/.zshrc to fill in your actual values
```

### `example-usage.sh`
Comprehensive script demonstrating all major features of Linear CLI:

```bash
# Make it executable
chmod +x examples/example-usage.sh

# Run it (make sure LINEAR_CLI_TOKEN is set first)
./examples/example-usage.sh
```

## Quick Examples

### Create Issues

```bash
# Simple issue
linear-cli create --title "Fix the homepage bug"

# With description
linear-cli create \
  --title "Add user profile page" \
  --description "Users should be able to view and edit their profile"

# Using bug template
linear-cli create \
  --title "Checkout fails on mobile" \
  --template bug \
  --priority 1

# Using feature template
linear-cli create \
  --title "Dark mode support" \
  --template feature
```

### View and Search

```bash
# List all issues
linear-cli list

# List with limit
linear-cli list --limit 10

# List for specific team
linear-cli list --team-id "TEAM-abc123"

# Search
linear-cli search "authentication"

# Show specific issue
linear-cli show ABC-123
```

### With Logging

```bash
# Enable logging
linear-cli --log create --title "Test issue"

# With verbose output
linear-cli --log --verbose list

# Custom log file
linear-cli --log --log-file /tmp/debug.log create --title "Debug this"
```

## Integration Examples

### Git Hook (Pre-commit)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Automatically create Linear issue for TODO comments

# Find TODOs in staged files
TODOS=$(git diff --cached --name-only | xargs grep -h "TODO:" 2>/dev/null)

if [ ! -z "$TODOS" ]; then
    echo "Found TODO items:"
    echo "$TODOS"

    # Optional: Create issues for each TODO
    # while IFS= read -r todo; do
    #     linear-cli create --title "$todo"
    # done <<< "$TODOS"
fi
```

### CI/CD Pipeline

```yaml
# Example GitHub Actions workflow
name: Create Linear Issue on Failed Build

on:
  workflow_run:
    workflows: ["CI"]
    types:
      - completed

jobs:
  create-issue:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install Linear CLI
        run: |
          pip install linear-cli
      - name: Create Issue
        env:
          LINEAR_CLI_TOKEN: ${{ secrets.LINEAR_TOKEN }}
        run: |
          linear-cli create \
            --title "Build failed: ${{ github.workflow }}" \
            --description "Build failed in ${{ github.repository }}" \
            --template bug \
            --priority 1
```

### Shell Alias

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Quick aliases for common operations
alias lc="linear-cli"
alias lcl="linear-cli list"
alias lcs="linear-cli search"
alias lcc="linear-cli create"

# Function to create bug quickly
bug() {
    linear-cli create --title "$*" --template bug --priority 1
}

# Function to create feature request
feature() {
    linear-cli create --title "$*" --template feature
}

# Usage:
# bug "Login button not working"
# feature "Add export to PDF"
```

## Tips

1. **Set up aliases** for frequently used commands
2. **Use templates** to maintain consistency
3. **Enable logging** during development and debugging
4. **Store tokens securely** in environment variables, not in scripts
5. **Use team IDs** to filter issues for your team
6. **Combine with other tools** like `jq` for JSON processing

## Need Help?

- See the main [README.md](../README.md) for full documentation
- Check [QUICKSTART.md](../QUICKSTART.md) for a quick introduction
- Run `linear-cli --help` for command-line help
