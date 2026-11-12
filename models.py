from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, user_id, name, email):
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID must be a positive integer.")

        self._user_id = user_id
        self._active = True
        self.name = name
        self.email = email

    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self.ensure_active()
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self.ensure_active()
        if not isinstance(value, str) or "@" not in value or " " in value:
            raise ValueError("Enter a valid email address.")
        self._email = value.strip()

    @property
    def active(self):
        return self._active

    def ensure_active(self):
        if not self._active:
            raise PermissionError("This account is inactive.")

    def update_email(self, new_email):
        self.ensure_active()
        self.email = new_email

    def _set_active(self, active):
        self._active = bool(active)

    @abstractmethod
    def get_permissions(self):
        """Each concrete user type must define its own permissions."""
        raise NotImplementedError


class ProfessionalProfile:
    def __init__(self, summary="", education="", skills=None):
        self._summary = ""
        self._education = ""
        self._skills = []
        self.update(summary, education, skills or [])

    @property
    def summary(self):
        return self._summary

    @property
    def education(self):
        return self._education

    @property
    def skills(self):
        return tuple(self._skills)

    def update(self, summary, education, skills):
        if not isinstance(summary, str) or not isinstance(education, str):
            raise ValueError("Summary and education must be text.")
        if not all(isinstance(skill, str) and skill.strip() for skill in skills):
            raise ValueError("Each skill must be a non-empty text value.")

        self._summary = summary.strip()
        self._education = education.strip()
        self._skills = [skill.strip() for skill in skills]
