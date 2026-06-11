import json
import logging
from pathlib import Path
from typing import Optional
from models import User, Project, Task

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


class JSONStore:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data = {"users": []}
        self._load()

    def _load(self):
        if not self.path.exists():
            self._save()
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                self._data = raw
        except Exception:
            # malformed or unreadable data -> reset
            logger.exception("Failed to load JSON data, resetting storage")
            self._data = {"users": []}
            self._save()

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)
        logger.debug("Saved data to %s", str(self.path))

    @property
    def users(self):
        return [User.from_dict(u) for u in self._data.get("users", [])]

    def add_user(self, user: User):
        self._data.setdefault("users", []).append(user.to_dict())
        self._save()
        logger.debug("Added user: %s", user)

    def find_user(self, name: str) -> Optional[User]:
        for u in self._data.get("users", []):
            if u.get("name") == name:
                return User.from_dict(u)
        return None

    def update_user(self, user: User):
        for i, u in enumerate(self._data.get("users", [])):
            if u.get("id") == user.id:
                self._data["users"][i] = user.to_dict()
                self._save()
                return
        logger.debug("Updated user: %s", user)

    def complete_task(self, project_title: str, task_title: str, owner_name: Optional[str] = None) -> bool:
        # find project
        owner = None
        proj = None
        if owner_name:
            owner = self.find_user(owner_name)
            if not owner:
                return False
            proj = next((p for p in owner.projects if p.title == project_title), None)
        else:
            for u in self.users:
                p = next((pp for pp in u.projects if pp.title == project_title), None)
                if p:
                    proj = p
                    owner = u
                    break
        if not proj:
            return False
        t = next((tt for tt in proj.tasks if tt.title == task_title), None)
        if not t:
            return False
        t.status = "done"
        self.update_user(owner)
        return True

    def save(self):
        self._save()
