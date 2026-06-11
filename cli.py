import os
import uuid
import json
import click
from pathlib import Path

from storage import DataStore

DB_PATH = os.environ.get("CLI_DB") or str(Path(__file__).parent / "data.json")
ds = DataStore(DB_PATH)


@click.group()
def cli():
    """Simple CLI for managing users, projects, and tasks."""


@cli.command(name="add-user")
@click.option("--name", required=True, help="User name")
def add_user(name):
    if ds.find_user(name):
        click.echo(f"User '{name}' already exists")
        return
    ds.add_user({"id": str(uuid.uuid4()), "name": name, "projects": []})
    click.echo(f"Added user '{name}'")


@cli.command(name="add-project")
@click.option("--user", required=True, help="Owner user name")
@click.option("--title", required=True, help="Project title")
def add_project(user, title):
    u = ds.find_user(user)
    if not u:
        click.echo(f"User '{user}' not found")
        return
    if any(p["title"] == title for p in u["projects"]):
        click.echo(f"Project '{title}' already exists for user '{user}'")
        return
    project = {"id": str(uuid.uuid4()), "title": title, "tasks": []}
    u["projects"].append(project)
    ds.save()
    click.echo(f"Added project '{title}' for user '{user}'")


@cli.command(name="add-task")
@click.option("--project", required=True, help="Project title")
@click.option("--title", required=True, help="Task title")
@click.option("--user", required=False, help="Owner user name (optional if project titles unique)")
def add_task(project, title, user):
    proj = ds.find_project(project, user)
    if not proj:
        click.echo(f"Project '{project}' not found")
        return
    if any(t["title"] == title for t in proj["tasks"]):
        click.echo(f"Task '{title}' already exists in project '{project}'")
        return
    task = {"id": str(uuid.uuid4()), "title": title, "completed": False}
    proj["tasks"].append(task)
    ds.save()
    click.echo(f"Added task '{title}' to project '{project}'")


@cli.command(name="list-users")
def list_users():
    for u in ds.data["users"]:
        click.echo(u["name"])


@cli.command(name="list-projects")
@click.option("--user", required=False, help="Filter by user name")
def list_projects(user):
    users = [ds.find_user(user)] if user else ds.data["users"]
    for u in users:
        if not u:
            click.echo(f"User '{user}' not found")
            return
        for p in u["projects"]:
            click.echo(f"{p['title']} (owner: {u['name']})")


@cli.command(name="list-tasks")
@click.option("--project", required=True, help="Project title")
@click.option("--user", required=False, help="User name if needed")
def list_tasks(project, user):
    proj = ds.find_project(project, user)
    if not proj:
        click.echo(f"Project '{project}' not found")
        return
    for t in proj["tasks"]:
        status = "done" if t.get("completed") else "todo"
        click.echo(f"{t['title']} [{status}]")


@cli.command(name="update-user")
@click.option("--old-name", required=True)
@click.option("--new-name", required=True)
def update_user(old_name, new_name):
    u = ds.find_user(old_name)
    if not u:
        click.echo(f"User '{old_name}' not found")
        return
    u["name"] = new_name
    ds.save()
    click.echo(f"Renamed user '{old_name}' -> '{new_name}'")


@cli.command(name="update-project")
@click.option("--user", required=True)
@click.option("--old-title", required=True)
@click.option("--new-title", required=True)
def update_project(user, old_title, new_title):
    u = ds.find_user(user)
    if not u:
        click.echo(f"User '{user}' not found")
        return
    p = next((pp for pp in u["projects"] if pp["title"] == old_title), None)
    if not p:
        click.echo(f"Project '{old_title}' not found for user '{user}'")
        return
    p["title"] = new_title
    ds.save()
    click.echo(f"Renamed project '{old_title}' -> '{new_title}'")


@cli.command(name="update-task")
@click.option("--project", required=True)
@click.option("--title", required=True)
@click.option("--new-title", required=False)
@click.option("--complete/--incomplete", default=None)
@click.option("--user", required=False)
def update_task(project, title, new_title, complete, user):
    proj = ds.find_project(project, user)
    if not proj:
        click.echo(f"Project '{project}' not found")
        return
    t = next((tt for tt in proj["tasks"] if tt["title"] == title), None)
    if not t:
        click.echo(f"Task '{title}' not found in project '{project}'")
        return
    if new_title:
        t["title"] = new_title
    if complete is not None:
        t["completed"] = bool(complete)
    ds.save()
    click.echo(f"Updated task '{title}'")


if __name__ == "__main__":
    cli()
