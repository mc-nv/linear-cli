# Linear CLI

A command-line interface for Linear - streamline your issue management workflow from the terminal.

## Features

- **Create issues** with customizable templates
- **Show issue details** by ID or identifier
- **List issues** with filtering options
- **Search issues** across your workspace
- **Template support** for standardized issue creation
- **Logging capabilities** for debugging and audit trails
- **Environment variable configuration** for easy setup

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/linear-cli.git
cd linear-cli

# Install in development mode
pip install -e .

# Or build and install the wheel
python -m pip install build
python -m build
pip install dist/linear_cli-0.1.0-py3-none-any.whl
```

### From PyPI (when published)

```bash
pip install linear-cli
```

## Configuration

### API Token

Linear CLI requires a Linear API token to authenticate. You can obtain one from your [Linear settings](https://linear.app/settings/api).

Set your token using one of these methods:

1. **Environment variable** (recommended):
   ```bash
   export LINEAR_CLI_TOKEN="your-api-token-here"
   ```

2. **Command-line argument**:
   ```bash
   linear-cli create --token "your-api-token-here" --title "New issue"
   ```

### Environment Variables

All configuration can be set via environment variables with the `LINEAR_CLI_` prefix:

| Variable | Description | Default |
|----------|-------------|---------|
| `LINEAR_CLI_TOKEN` | Linear API token (required) | - |
| `LINEAR_CLI_TEAM_ID` | Default team ID for operations | - |
| `LINEAR_CLI_TEMPLATE` | Default template name | - |
| `LINEAR_CLI_LOG_FILE` | Custom log file path | `linear-cli.log` |

Example `.env` file:
```bash
LINEAR_CLI_TOKEN=lin_api_xxxxxxxxxxxxx
LINEAR_CLI_TEAM_ID=12345678-1234-1234-1234-123456789abc
LINEAR_CLI_TEMPLATE=default
```

## Usage

### Global Options

```bash
linear-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --log              Enable logging to file
  --log-file TEXT    Log file path (default: linear-cli.log)
  --verbose          Enable verbose output
  --template TEXT    Template name to use
  --help             Show this message and exit
```

### Commands

#### Create an Issue

```bash
# Basic usage
linear-cli create --title "Fix login bug"

# With description
linear-cli create --title "Add new feature" --description "Detailed description here"

# With all options
linear-cli create \
  --title "Bug in payment flow" \
  --description "Users can't complete checkout" \
  --team-id "TEAM-123" \
  --priority 1 \
  --labels "bug,urgent"

# Using a template
linear-cli create --title "Critical bug" --template bug

# With logging
linear-cli --log --verbose create --title "New task"
```

**Options:**
- `-t, --title TEXT` - Issue title (required)
- `-d, --description TEXT` - Issue description
- `--team-id TEXT` - Team ID
- `--priority INTEGER` - Priority (0-4, where 0 is highest)
- `--labels TEXT` - Comma-separated list of label IDs
- `--template TEXT` - Template name to use
- `--token TEXT` - Linear API token

#### Show Issue Details

```bash
# By issue ID
linear-cli show ABC-123

# By issue identifier
linear-cli show 12345678-1234-1234-1234-123456789abc
```

**Arguments:**
- `ISSUE_ID` - Issue ID or identifier (required)

**Options:**
- `--token TEXT` - Linear API token

#### List Issues

```bash
# List all issues (default limit: 50)
linear-cli list

# List issues for a specific team
linear-cli list --team-id "TEAM-123"

# Customize the limit
linear-cli list --limit 100
```

**Options:**
- `--team-id TEXT` - Filter by team ID
- `--limit INTEGER` - Maximum number of issues to return (default: 50)
- `--token TEXT` - Linear API token

#### Search Issues

```bash
# Basic search
linear-cli search "authentication"

# Search with limit
linear-cli search "bug" --limit 20
```

**Arguments:**
- `QUERY` - Search query string (required)

**Options:**
- `--limit INTEGER` - Maximum number of results (default: 50)
- `--token TEXT` - Linear API token

#### My Issues

```bash
# List issues assigned to you
linear-cli my-issues

# List with limit
linear-cli my-issues --limit 10

# Output in JSON format
linear-cli my-issues --json

# JSON with limit
linear-cli my-issues --limit 20 --json
```

**Options:**
- `--limit INTEGER` - Maximum number of issues to return (default: 50)
- `--json` - Output in JSON format
- `--token TEXT` - Linear API token

**JSON Output Example:**
```json
{
  "count": 2,
  "issues": [
    {
      "id": "12345678-1234-1234-1234-123456789abc",
      "identifier": "ABC-123",
      "title": "Fix login bug",
      "description": "Users cannot login",
      "priority": 1,
      "url": "https://linear.app/team/issue/ABC-123",
      "state": {
        "name": "In Progress"
      },
      "dueDate": "2025-10-15",
      "createdAt": "2025-10-07T10:00:00.000Z",
      "updatedAt": "2025-10-07T12:00:00.000Z"
    }
  ]
}
```

### Templates

Linear CLI supports templates for creating issues with predefined structures. Built-in templates:

#### Default Template
Basic issue structure with customizable fields.

#### Bug Template
```bash
linear-cli create --title "Login fails on mobile" --template bug
```
Creates an issue with:
- Title prefixed with `[BUG]`
- Structured description with sections for steps to reproduce, expected behavior, and actual behavior
- Priority set to 1 (urgent)
- Automatically tagged with "bug" label

#### Feature Template
```bash
linear-cli create --title "Add dark mode" --template feature
```
Creates an issue with:
- Title prefixed with `[FEATURE]`
- Structured description with sections for use case and proposed solution
- Priority set to 3 (medium)
- Automatically tagged with "feature" label

### Examples

#### Daily Workflow

```bash
# Set your environment variables once
export LINEAR_CLI_TOKEN="lin_api_xxxxxxxxxxxxx"
export LINEAR_CLI_TEAM_ID="12345678-1234-1234-1234-123456789abc"

# Check issues assigned to you
linear-cli my-issues

# Get your issues in JSON format for automation
linear-cli my-issues --json

# Create a bug report
linear-cli create \
  --title "Login button not responding" \
  --template bug \
  --priority 1

# Check your issues
linear-cli list --limit 10

# Search for specific issues
linear-cli search "login"

# Get details on a specific issue
linear-cli show ABC-123
```

#### With Logging

```bash
# Enable logging for debugging
linear-cli --log --verbose create --title "Test issue"

# Check the log file
cat linear-cli.log
```

#### Using Custom Log File

```bash
# Specify custom log file location
linear-cli --log --log-file /tmp/my-linear.log list

# Or via environment variable
export LINEAR_CLI_LOG_FILE="/tmp/my-linear.log"
linear-cli --log list
```

## Development

### Project Structure

```
linear-cli/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Main CLI entry point
│   ├── client.py            # Linear API client
│   ├── utils.py             # Utility functions
│   └── commands/            # Command implementations
│       ├── __init__.py
│       ├── create.py        # Create command
│       ├── show.py          # Show command
│       ├── list.py          # List command
│       └── search.py        # Search command
├── setup.py                 # Package setup (legacy)
├── pyproject.toml          # Modern package configuration
├── requirements.txt        # Dependencies
└── README.md              # This file
```

### Building

```bash
# Install build tools
pip install build wheel

# Build the package
python -m build

# This creates:
# - dist/linear_cli-0.1.0-py3-none-any.whl
# - dist/linear-cli-0.1.0.tar.gz
```

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run tests (when added)
pytest

# With coverage
pytest --cov=src
```

## Architecture

### Client Module (`src/client.py`)
- Handles all communication with the Linear GraphQL API
- Manages authentication via API token
- Provides methods for creating, fetching, listing, and searching issues
- Error handling and response validation

### Commands (`src/commands/`)
Each command is implemented in a separate file for maintainability:
- **create.py** - Issue creation with template support
- **show.py** - Display detailed issue information
- **list.py** - List issues with filtering
- **search.py** - Search across issues

### Utilities (`src/utils.py`)
- Logging configuration
- Template management
- Configuration value resolution (CLI > Environment > Default)
- Issue formatting for display

## Troubleshooting

### Authentication Errors

```
Error: Linear API token is required.
```

**Solution:** Set your API token:
```bash
export LINEAR_CLI_TOKEN="your-token-here"
```

### GraphQL Errors

```
Error: GraphQL errors: Unauthorized
```

**Solution:** Check that your API token is valid and has the necessary permissions.

### Module Not Found

```
ModuleNotFoundError: No module named 'src'
```

**Solution:** Install the package properly:
```bash
pip install -e .
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests and linting
5. Commit your changes: `git commit -am 'Add new feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/yourusername/linear-cli).

## Changelog

### Version 0.1.0
- Initial release
- Basic CRUD operations for issues
- Template support
- Logging capabilities
- Environment variable configuration
