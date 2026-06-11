from typing import List, Optional


class Project:
    _id_counter = 1

    def __init__(self, title: str, description: str = "", due_date: Optional[str] = None, id: Optional[int] = None, tasks: Optional[List['Task']] = None):
        if id is None:
            self.id = Project._id_counter
            Project._id_counter += 1
        else:
            self.id = id
            try:
                if int(id) >= Project._id_counter:
                    Project._id_counter = int(id) + 1
            except Exception:
                pass
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks: List['Task'] = tasks or []

    def add_task(self, task: 'Task'):
        self.tasks.append(task)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, d):
        from .task import Task

        tasks = [Task.from_dict(t) for t in d.get("tasks", [])]
        return cls(title=d.get("title"), description=d.get("description"), due_date=d.get("due_date"), id=d.get("id"), tasks=tasks)

    def __repr__(self):
        return f"Project(id={self.id}, title={self.title})"
