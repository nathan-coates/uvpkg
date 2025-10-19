# uvpkg

Quick build uv packaged app starter.

This small CLI helps initialize a new "uv" package in a user-configured programming directory. It wraps the `uv init --package <name>` command and stores a configuration file under macOS Application Support.

## Key features

- Reads/writes a simple `config.json` under "Application Support/uvpkg" to store a `programming_dir` path.
- Verifies the `uv` command-line tool is available in PATH before running.
- Prevents overwriting an existing package.

## Requirements

- Python 3.9+
- The `uv` CLI tool available on your PATH
- The `plumbum` library (declared in `pyproject.toml`)

## Installation

Install from source (editable) for development:

```bash
python -m pip install -e .
```

Or build and install a wheel per your normal workflow.

## Usage

After installation the package exposes a console script `uvpkg` (see `pyproject.toml`). Run:

```bash
uvpkg <package-name>
```

What it does:

- Ensures `uv` is installed.
- Ensures a configuration file exists at `~/Library/Application Support/uvpkg/config.json` which contains a single key `programming_dir` with the path where new packages will be created.
- Runs `uv init --package <package-name>` in the configured programming directory.

If the config file doesn't exist the CLI will prompt you to enter the programming directory path. The config is then saved for subsequent runs.

## Configuration

Config location (macOS):

```
~/Library/Application Support/uvpkg/config.json
```

Contents example:

```json
{
	"programming_dir": "/Users/you/Projects"
}
```

## Development

- Project: `uvpkg`
- Version: 0.1.0

Run the CLI locally (without installing) from the repo root:

```bash
python -m src.uvpkg <package-name>
```

or run the module directly if set up as a package:

```bash
python -m uvpkg <package-name>
```

## Notes

- The code currently targets macOS for the Application Support path. If you want cross-platform support, update `get_application_support_dir` to handle Linux/Windows conventions.
- The package relies on the external `uv` executable; consider adding a helpful link to its documentation in this README if available.

---

Generated README based on package metadata and the source code in `src/uvpkg`.
