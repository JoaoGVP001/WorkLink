from enum import Enum, auto


class ApplicationStatus(Enum):
    SENT = auto()
    UNDER_REVIEW = auto()
    APPROVED = auto()
    REJECTED = auto()
    CANCELLED = auto()


class VacancyStatus(Enum):
    OPEN = auto()
    CLOSED = auto()


class UserRole(Enum):
    RECRUITER = auto()
    ADMINISTRATOR = auto()
