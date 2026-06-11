import json
from pathlib import Path


class DataStore:
    def __init__(self, path):
        self.path = Path(path)
        self.data = {"users": []}
        self._load()

    def _load(self):
        if not self.path.exists():
            self.save()
        else:
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {"users": []}
                self.save()

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def add_user(self, user_obj):
        self.data["users"].append(user_obj)
        self.save()

    def find_user(self, name):
        for u in self.data["users"]:
            if u.get("name") == name:
                return u
        return None

    def find_project(self, project_title, user_name=None):
        if user_name:
            u = self.find_user(user_name)
            if not u:
                return None
            return next((p for p in u.get("projects", []) if p.get("title") == project_title), None)
        for u in self.data["users"]:
            p = next((p for p in u.get("projects", []) if p.get("title") == project_title), None)
            if p:
                return p
        return None
