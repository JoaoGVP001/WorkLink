from abc import ABC, abstractmethod
from datetime import date

from enums import ApplicationStatus, UserRole, VacancyStatus


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


class Company:
    def __init__(self, name, tax_id):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Company name cannot be empty.")
        if not isinstance(tax_id, str) or not tax_id.strip():
            raise ValueError("Company tax ID cannot be empty.")

        self._name = name.strip()
        self._tax_id = tax_id.strip()
        self._recruiters = []
        self._vacancies = []

    @property
    def name(self):
        return self._name

    @property
    def tax_id(self):
        return self._tax_id

    @property
    def recruiters(self):
        return tuple(self._recruiters)

    @property
    def vacancies(self):
        return tuple(self._vacancies)

    def list_open_vacancies(self, today):
        return tuple(vacancy for vacancy in self._vacancies if vacancy.is_open(today))

    def _add_recruiter(self, recruiter):
        if recruiter not in self._recruiters:
            self._recruiters.append(recruiter)

    def _remove_recruiter(self, recruiter):
        if recruiter in self._recruiters:
            self._recruiters.remove(recruiter)

    def _add_vacancy(self, vacancy):
        if vacancy.company is not self:
            raise ValueError("A vacancy must belong to this company.")
        if vacancy not in self._vacancies:
            self._vacancies.append(vacancy)

    def _remove_vacancy(self, vacancy):
        if vacancy in self._vacancies:
            self._vacancies.remove(vacancy)


class Vacancy:
    def __init__(self, title, description, deadline, company):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Vacancy title cannot be empty.")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Vacancy description cannot be empty.")
        if not isinstance(deadline, date):
            raise ValueError("The deadline must be a date.")
        if company is None:
            raise ValueError("A vacancy must belong to a company.")

        self._title = title.strip()
        self._description = description.strip()
        self._deadline = deadline
        self._status = VacancyStatus.OPEN
        self._company = company
        self._applications = []

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def deadline(self):
        return self._deadline

    @property
    def status(self):
        return self._status

    @property
    def company(self):
        return self._company

    @property
    def applications(self):
        return tuple(self._applications)

    def is_open(self, today):
        self._check_date(today)
        return self._status == VacancyStatus.OPEN and today <= self._deadline

    def update(self, recruiter, title, description, deadline, today):
        self._check_manager(recruiter)
        self._check_date(today)
        if self._status != VacancyStatus.OPEN:
            raise ValueError("A closed vacancy cannot be updated.")
        if not isinstance(deadline, date) or deadline < today:
            raise ValueError("The new deadline must be today or a future date.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Vacancy title cannot be empty.")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Vacancy description cannot be empty.")

        self._title = title.strip()
        self._description = description.strip()
        self._deadline = deadline

    def close(self, recruiter):
        self._check_manager(recruiter)
        self._status = VacancyStatus.CLOSED

    def can_be_deleted(self, recruiter):
        self._check_manager(recruiter)
        return len(self._applications) == 0

    def _check_manager(self, recruiter):
        recruiter.ensure_active()
        if recruiter.company is not self._company:
            raise PermissionError("This recruiter does not manage this company's vacancies.")

    @staticmethod
    def _check_date(value):
        if not isinstance(value, date):
            raise ValueError("A date value is required.")

    def _add_application(self, application):
        if application not in self._applications:
            self._applications.append(application)


class Candidate(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self._profile = ProfessionalProfile()
        self._applications = []

    @property
    def profile(self):
        return self._profile

    @property
    def applications(self):
        return tuple(self._applications)

    def get_permissions(self):
        return {"view_open_vacancies", "manage_own_profile", "apply_for_vacancies"}

    def update_profile(self, summary, education, skills):
        self.ensure_active()
        self._profile.update(summary, education, skills)

    def apply_to(self, vacancy, today):
        self.ensure_active()
        return Application(self, vacancy, today)

    def list_applications(self):
        self.ensure_active()
        return tuple(self._applications)

    def cancel_application(self, application):
        self.ensure_active()
        if application.candidate is not self:
            raise PermissionError("A candidate can only cancel their own application.")
        application.cancel(self)

    def _add_application(self, application):
        if application not in self._applications:
            self._applications.append(application)


class Recruiter(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self._company = None

    @property
    def company(self):
        return self._company

    def get_permissions(self):
        return {"manage_company_vacancies", "review_applications"}

    def create_vacancy(self, title, description, deadline, today):
        self.ensure_active()
        if not isinstance(today, date):
            raise ValueError("A date value is required.")
        if not isinstance(deadline, date) or deadline < today:
            raise ValueError("The deadline must be today or a future date.")
        if self._company is None:
            raise ValueError("Link this recruiter to a company first.")
        vacancy = Vacancy(title, description, deadline, self._company)
        self._company._add_vacancy(vacancy)
        return vacancy

    def list_applications(self, vacancy):
        self.ensure_active()
        vacancy._check_manager(self)
        return vacancy.applications

    def review_application(self, application, new_status):
        self.ensure_active()
        application.change_status(self, new_status)

    def update_vacancy(self, vacancy, title, description, deadline, today):
        vacancy.update(self, title, description, deadline, today)

    def close_vacancy(self, vacancy):
        vacancy.close(self)

    def remove_vacancy(self, vacancy):
        self.ensure_active()
        if not vacancy.can_be_deleted(self):
            raise ValueError("A vacancy with applications cannot be deleted; close it instead.")
        self._company._remove_vacancy(vacancy)

    def _set_company(self, company):
        self._company = company


class Administrator(User):
    def get_permissions(self):
        return {"manage_users", "manage_companies", "manage_recruiter_links"}

    def create_company(self, name, tax_id):
        self.ensure_active()
        return Company(name, tax_id)

    def create_privileged_account(self, user_id, name, email, role):
        self.ensure_active()
        if role == UserRole.RECRUITER:
            return Recruiter(user_id, name, email)
        if role == UserRole.ADMINISTRATOR:
            return Administrator(user_id, name, email)
        raise ValueError("Only recruiter and administrator accounts are privileged.")

    def list_users(self, users):
        self.ensure_active()
        return tuple(users)

    def set_account_active(self, target, active):
        self.ensure_active()
        if target is self and not active:
            raise ValueError("An administrator cannot deactivate their own account.")
        target._set_active(active)

    def assign_recruiter(self, recruiter, company):
        self.ensure_active()
        if not isinstance(recruiter, Recruiter):
            raise ValueError("Only a recruiter can be linked to a company.")
        if company is not None and not isinstance(company, Company):
            raise ValueError("Choose a valid company or None.")
        recruiter.ensure_active()
        old_company = recruiter.company
        if old_company is company:
            return
        if old_company is not None:
            old_company._remove_recruiter(recruiter)
        recruiter._set_company(company)
        if company is not None:
            company._add_recruiter(recruiter)


class Application:
    def __init__(self, candidate, vacancy, registered_on):
        if not isinstance(registered_on, date):
            raise ValueError("The registration date must be a date.")
        candidate.ensure_active()
        if not vacancy.is_open(registered_on):
            raise ValueError("Applications are only accepted while the vacancy is open and within its deadline.")
        if any(existing.vacancy is vacancy for existing in candidate.applications):
            raise ValueError("This candidate has already applied for this vacancy.")

        self._candidate = candidate
        self._vacancy = vacancy
        self._registered_on = registered_on
        self._status = ApplicationStatus.SENT
        candidate._add_application(self)
        vacancy._add_application(self)

    @property
    def candidate(self):
        return self._candidate

    @property
    def vacancy(self):
        return self._vacancy

    @property
    def registered_on(self):
        return self._registered_on

    @property
    def status(self):
        return self._status

    def cancel(self, candidate):
        candidate.ensure_active()
        if candidate is not self._candidate:
            raise PermissionError("Only the candidate who applied can cancel this application.")
        pending = {ApplicationStatus.SENT, ApplicationStatus.UNDER_REVIEW}
        if self._status not in pending:
            raise ValueError("Only a pending application can be cancelled.")
        self._status = ApplicationStatus.CANCELLED

    def change_status(self, recruiter, new_status):
        recruiter.ensure_active()
        if not isinstance(new_status, ApplicationStatus):
            raise ValueError("Choose a valid application status.")
        if recruiter.company is not self._vacancy.company:
            raise PermissionError("Only a recruiter from the vacancy's company can review it.")

        allowed_changes = {
            ApplicationStatus.SENT: {ApplicationStatus.UNDER_REVIEW, ApplicationStatus.REJECTED},
            ApplicationStatus.UNDER_REVIEW: {ApplicationStatus.APPROVED, ApplicationStatus.REJECTED},
        }
        if new_status not in allowed_changes.get(self._status, set()):
            raise ValueError("This application status change is not allowed.")
        self._status = new_status
