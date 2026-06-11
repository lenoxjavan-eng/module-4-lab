import os
import tempfile
from utils.storage import JSONStore
from models.user import User
from models.project import Project
from models.task import Task


def test_storage_add_and_find_user(tmp_path):
    fp = tmp_path / "data.json"
    store = JSONStore(str(fp))
    u = User(name="Bob", email="bob@example.com")
    store.add_user(u)
    found = store.find_user("Bob")
    assert found is not None
    assert found.name == "Bob"


def test_complete_task_flow(tmp_path):
    fp = tmp_path / "data.json"
    store = JSONStore(str(fp))
    u = User(name="Carol", email="carol@example.com")
    p = Project(title="ProjX")
    t = Task(title="Fix bug")
    p.add_task(t)
    u.add_project(p)
    store.add_user(u)

    ok = store.complete_task("ProjX", "Fix bug", owner_name="Carol")
    assert ok
    f = store.find_user("Carol")
    assert f.projects[0].tasks[0].status == "done"
