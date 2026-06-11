# CLI Manager

Simple Python CLI to manage users, projects, and tasks.

## Setup

- Recommended: create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the CLI

- Default data file: `data/data.json` in the repository root. To change, set the `CLI_DB` environment variable.

Examples:

```bash
python main.py add-user --name "Alex" --email "alex@example.com"
python main.py add-project --user "Alex" --title "CLI Tool" --description "Tooling" --due-date "2026-06-30"
python main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alex" --user Alex

python main.py list-users
python main.py list-projects --user "Alex"
python main.py list-tasks --project "CLI Tool" --user "Alex"
python main.py complete-task --project "CLI Tool" --task "Implement add-task" --user Alex
```

CLI commands available (partial):
- `add-user` — create a new user with name and email
- `list-projects` — list projects (optionally for a single user)
- `complete-task` — mark a task done (provide `--project` and `--task`, optionally `--user`)

Full CLI is implemented in `main.py`.

## Project Structure

- `main.py` — CLI entry point (argparse)
- `models/` — `User`, `Project`, `Task` classes with serialization
- `utils/storage.py` — `JSONStore` for loading/saving data
- `data/` — default JSON data file location
- `tests/` — unit tests for models, storage, and CLI helpers

## Features

- Object-oriented models with validation and serialization.
- JSON persistence with resilient load/save (handles malformed data by resetting).
- Argparse-based CLI with `rich` for pretty terminal output.
- Unit tests (pytest) for models, storage, and CLI helpers.
- Logging in `utils/storage.py` for tracing I/O operations.

## Running Tests

Install test dependencies and run:

```bash
pip install -r requirements.txt
pytest -q
```

If you don't want to install `pytest`, you can run the individual test scripts manually or use the CLI to exercise behavior.

## Known Issues & Notes

- Some CLI subcommands (like `add-project` and `add-task`) were previously implemented with `click` in `cli.py` and may still exist; the authoritative CLI is `main.py` (argparse).
- Tests and `pip` may not be available in all environments (CI runners or minimal containers). Install `pip`/`pytest` before running tests.
- `data/data.json` will be reset if malformed JSON is detected — there is no automatic backup yet.
- Project and task title uniqueness is enforced per-user only when using owner hints; ambiguous project titles across users may pick the first match.

## Contributing

Open a PR with changes. Run tests and ensure formatting remains consistent.

---

For more details, see `main.py` and `utils/storage.py`.
