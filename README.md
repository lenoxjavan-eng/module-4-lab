# CLI Manager

Simple Python CLI to manage users, projects, and tasks.

Usage examples:

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the CLI:

```bash
python main.py add-user --name "Alex" --email "alex@example.com"
python main.py add-project --user "Alex" --title "CLI Tool" --description "Tooling"
python main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alex"
```

List commands:

```bash
python main.py list-users
python main.py list-projects --user "Alex"
python main.py list-tasks --project "CLI Tool" --user "Alex"

Notes:
- Data is saved to `data.json` in the project folder by default. Set `CLI_DB` env var to change path.
