from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .project import Project


class Person:
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value


class User(Person):
    _id_counter = 1

    def __init__(self, name: str, email: str, id: Optional[int] = None, projects: Optional[List['Project']] = None):
        super().__init__(name)
        self._email = email
        if id is None:
            self.id = User._id_counter
            User._id_counter += 1
        else:
            self.id = id
            try:
                if int(id) >= User._id_counter:
                    User._id_counter = int(id) + 1
            except Exception:
                pass
        self.projects: List['Project'] = projects or []

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not value or "@" not in value:
            raise ValueError("Invalid email")
        self._email = value

    def add_project(self, project: 'Project'):
        self.projects.append(project)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "projects": [p.to_dict() for p in self.projects],
        }

    @classmethod
    def from_dict(cls, d):
        from .project import Project

        projects = [Project.from_dict(p) for p in d.get("projects", [])]
        return cls(name=d.get("name"), email=d.get("email"), id=d.get("id"), projects=projects)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"
