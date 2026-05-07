# Linear CLI

Command-line interface for the Linear API.

## Installation

Requires Python 3.8 or newer.

### From source (editable)

```bash
git clone https://github.com/mc-nv/linear-cli.git
cd linear-cli
pip install -e .
```

### From a built wheel

```bash
pip install build
python -m build
pip install dist/linear_cli-0.2.0-py3-none-any.whl
```

After installation, the `linear` command is available on your `PATH`.

## Configuration

Set your Linear API token via env var or config file:

```bash
export LINEAR_CLI_TOKEN="lin_api_xxxxxxxxxxxxx"
```

Or place a JSON config at `~/.config/linear/user/conf.json`:

```json
{
  "LINEAR_CLI_TOKEN": "lin_api_xxxxxxxxxxxxx",
  "LINEAR_CLI_USER_DATA_QUERIES": "~/my-linear-queries"
}
```

Override the config path with `LINEAR_CLI_CONFIG` (supports multiple paths
separated by `:`, with later paths overriding earlier ones). Real env vars
always take precedence over config files.

Inspect the resolved configuration and where each value came from:

```bash
linear config get
```

## Usage

```bash
linear ping                  # check API connectivity
linear query list            # list available query templates
linear query my-issues       # run a built-in query
linear config get            # show resolved configuration
```

User-defined GraphQL templates can be loaded from a directory pointed to by
`LINEAR_CLI_USER_DATA_QUERIES`; user templates override built-in ones with
the same name.
