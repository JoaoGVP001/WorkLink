from models import Administrator, Candidate, Company, Recruiter
from enums import UserRole


class WorklinkService:
    """Keeps the system's objects in memory for this project version."""

    def __init__(self):
        self._users = []
        self._companies = []
        self._next_user_id = 1

    @property
    def users(self):
        return tuple(self._users)

    @property
    def companies(self):
        return tuple(self._companies)

    def create_initial_admin(self, name, email):
        if any(isinstance(user, Administrator) for user in self._users):
            raise ValueError("The initial administrator has already been created.")
        admin = Administrator(self._new_user_id(), name, email)
        self._users.append(admin)
        return admin

    def register_candidate(self, name, email):
        candidate = Candidate(self._new_user_id(), name, email)
        self._users.append(candidate)
        return candidate

    def create_privileged_account(self, admin, name, email, role):
        if not isinstance(role, UserRole):
            raise ValueError("Choose a valid privileged account type.")
        user = admin.create_privileged_account(self._new_user_id(), name, email, role)
        self._users.append(user)
        return user

    def create_company(self, admin, name, tax_id):
        company = admin.create_company(name, tax_id)
        self._companies.append(company)
        return company

    def assign_recruiter(self, admin, recruiter, company):
        if not isinstance(recruiter, Recruiter):
            raise ValueError("Only a recruiter can be linked to a company.")
        if company is not None and not isinstance(company, Company):
            raise ValueError("Choose a valid company or None.")
        admin.assign_recruiter(recruiter, company)

    def list_users(self, admin):
        return admin.list_users(self._users)

    def list_open_vacancies(self, today):
        vacancies = []
        for company in self._companies:
            vacancies.extend(company.list_open_vacancies(today))
        return tuple(vacancies)

    def set_account_active(self, admin, target, active):
        admin.set_account_active(target, active)

    def _new_user_id(self):
        user_id = self._next_user_id
        self._next_user_id += 1
        return user_id
