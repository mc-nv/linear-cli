# Quick Start Guide

Get up and running with Linear CLI in minutes.

## 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/linear-cli.git
cd linear-cli

# Install the package
pip install -e .
```

Or using the Makefile:
```bash
make install-dev
```

## 2. Configuration

Get your Linear API token from [Linear Settings > API](https://linear.app/settings/api).

Set your token:
```bash
export LINEAR_CLI_TOKEN="lin_api_xxxxxxxxxxxxx"
```

For permanent configuration, add it to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
echo 'export LINEAR_CLI_TOKEN="lin_api_xxxxxxxxxxxxx"' >> ~/.zshrc
source ~/.zshrc
```

## 3. Basic Usage

### Create your first issue
```bash
linear-cli create --title "My first issue"
```

### List your issues
```bash
linear-cli list
```

### Search for issues
```bash
linear-cli search "bug"
```

### View issue details
```bash
linear-cli show ABC-123
```

## 4. Advanced Features

### Using Templates

Create a bug report:
```bash
linear-cli create --title "Login button broken" --template bug
```

Create a feature request:
```bash
linear-cli create --title "Add dark mode" --template feature
```

### Enable Logging

For debugging or keeping an audit trail:
```bash
linear-cli --log --verbose create --title "Test issue"
```

Check the log:
```bash
cat linear-cli.log
```

### Set Default Team

If you work with a specific team:
```bash
export LINEAR_CLI_TEAM_ID="your-team-id"
linear-cli list  # Now lists issues for your team by default
```

## 5. Build Package (Optional)

To build a distributable wheel:
```bash
make build
```

This creates a wheel file in `dist/` that you can distribute:
```bash
pip install dist/linear_cli-0.1.0-py3-none-any.whl
```

## 6. Common Workflows

### Morning Standup
```bash
# Check your assigned issues
linear-cli list --limit 10

# Create a new task
linear-cli create --title "Review PR #123"
```

### Bug Reporting
```bash
linear-cli create \
  --title "Payment processing fails for EU cards" \
  --template bug \
  --priority 1
```

### Sprint Planning
```bash
# Search for features
linear-cli search "feature"

# Create a new feature
linear-cli create \
  --title "Implement user notifications" \
  --template feature \
  --priority 3
```

## 7. Troubleshooting

**Command not found: linear-cli**
```bash
# Make sure the package is installed
pip install -e .

# Or check if it's in your PATH
which linear-cli
```

**Authentication error**
```bash
# Verify your token is set
echo $LINEAR_CLI_TOKEN

# Test with explicit token
linear-cli --token "your-token" list
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore all commands with `linear-cli --help`
- Customize templates in `src/utils.py`
- Set up your preferred environment variables

Happy issue tracking! 🚀
