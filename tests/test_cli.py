import os
import tempfile
from argparse import Namespace
from main import cmd_add_user, cmd_list_projects, cmd_complete_task
from utils.storage import JSONStore


def test_cli_add_and_list(tmp_path, capsys):
    # configure store to use tmp file
    os.environ["CLI_DB"] = str(tmp_path / "data.json")
    # add user
    args = Namespace(name="Dana", email="dana@example.com")
    cmd_add_user(args)
    # list projects (none) should not error
    args2 = Namespace(user=None)
    cmd_list_projects(args2)


def test_cli_complete_task(tmp_path):
    os.environ["CLI_DB"] = str(tmp_path / "data.json")
    # create store and objects
    store = JSONStore(os.environ["CLI_DB"])
    from models.user import User
    from models.project import Project
    from models.task import Task

    u = User(name="Eve", email="eve@example.com")
    p = Project(title="Alpha")
    t = Task(title="Do it")
    p.add_task(t)
    u.add_project(p)
    store.add_user(u)

    args = Namespace(project="Alpha", task="Do it", user="Eve")
    cmd_complete_task(args)
    f = store.find_user("Eve")
    assert f.projects[0].tasks[0].status == "done"
