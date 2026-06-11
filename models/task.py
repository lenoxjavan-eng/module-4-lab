class Task:
    _id_counter = 1

    def __init__(self, title: str, status: str = "todo", assigned_to: str = None, id: int = None):
        if id is None:
            self.id = Task._id_counter
            Task._id_counter += 1
        else:
            self.id = id
            try:
                if int(id) >= Task._id_counter:
                    Task._id_counter = int(id) + 1
            except Exception:
                pass
        self.title = title
        self._status = status
        self.assigned_to = assigned_to

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str):
        allowed = {"todo", "in-progress", "done"}
        if value not in allowed:
            raise ValueError(f"Invalid status '{value}'")
        self._status = value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(title=d.get("title"), status=d.get("status", "todo"), assigned_to=d.get("assigned_to"), id=d.get("id"))

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, status={self.status})"
