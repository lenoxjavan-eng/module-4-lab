import tempfile
import os
from models.user import User
from models.project import Project
from models.task import Task


def test_model_serialization_roundtrip():
    t = Task(title="T1", status="todo", assigned_to="Alex")
    p = Project(title="P1", description="Desc", due_date="2026-07-01", tasks=[t])
    u = User(name="Alex", email="alex@example.com", projects=[p])

    d = u.to_dict()
    u2 = User.from_dict(d)

    assert u2.name == "Alex"
    assert u2.email == "alex@example.com"
    assert len(u2.projects) == 1
    assert u2.projects[0].title == "P1"
    assert len(u2.projects[0].tasks) == 1
    assert u2.projects[0].tasks[0].title == "T1"
