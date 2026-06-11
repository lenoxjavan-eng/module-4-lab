import os
import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from models import User, Project, Task
from utils.storage import JSONStore


DATA_PATH = os.environ.get("CLI_DB") or str(Path(__file__).parent / "data" / "data.json")
store = JSONStore(DATA_PATH)
console = Console()


def cmd_add_user(args):
    if store.find_user(args.name):
        console.print(f"[red]User '{args.name}' exists[/red]")
        return
    u = User(name=args.name, email=args.email)
    store.add_user(u)
    console.print(f"[green]Added user {args.name}[/green]")


def cmd_list_projects(args):
    table = Table(title="Projects")
    table.add_column("ID", style="dim")
    table.add_column("Title")
    table.add_column("Owner")
    table.add_column("Due")
    if args.user:
        u = store.find_user(args.user)
        if not u:
            console.print(f"[red]User '{args.user}' not found[/red]")
            return
        for p in u.projects:
            table.add_row(str(p.id), p.title, u.name, str(p.due_date))
    else:
        for u in store.users:
            for p in u.projects:
                table.add_row(str(p.id), p.title, u.name, str(p.due_date))
    console.print(table)


def cmd_complete_task(args):
    ok = store.complete_task(args.project, args.task, owner_name=args.user)
    if ok:
        console.print(f"[green]Marked task '{args.task}' done in project '{args.project}'[/green]")
    else:
        console.print(f"[red]Failed to mark task. Check project/user/task names[/red]")


def build_parser():
    parser = argparse.ArgumentParser(prog="cli")
    sub = parser.add_subparsers()

    a = sub.add_parser("add-user")
    a.add_argument("--name", required=True)
    a.add_argument("--email", required=True)
    a.set_defaults(func=cmd_add_user)

    p = sub.add_parser("list-projects")
    p.add_argument("--user", required=False)
    p.set_defaults(func=cmd_list_projects)

    c = sub.add_parser("complete-task")
    c.add_argument("--project", required=True)
    c.add_argument("--task", required=True)
    c.add_argument("--user", required=False)
    c.set_defaults(func=cmd_complete_task)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
