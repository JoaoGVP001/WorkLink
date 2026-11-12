from datetime import date, timedelta

from enums import ApplicationStatus, UserRole
from services import WorklinkService


def main():
    today = date.today()
    service = WorklinkService()

    admin = service.create_initial_admin("Alex Admin", "admin@worklink.com")
    company = service.create_company(admin, "Northstar Tech", "12.345.678/0001-90")
    recruiter = service.create_privileged_account(
        admin, "Riley Recruiter", "riley@northstar.com", UserRole.RECRUITER
    )
    service.assign_recruiter(admin, recruiter, company)
    candidate = service.register_candidate("Casey Candidate", "casey@example.com")
    candidate.update_profile(
        "Interested in software development.",
        "Computer Science student",
        ["Python", "Problem solving"],
    )

    vacancy = recruiter.create_vacancy(
        "Junior Python Developer",
        "Help the team build and improve internal tools.",
        today + timedelta(days=7),
        today,
    )

    print("WORKLINK - example run")
    print("----------------------")
    print("User permissions:")
    for user in (candidate, recruiter, admin):
        print(f"- {user.name}: {', '.join(sorted(user.get_permissions()))}")

    print("\nOpen vacancies:")
    for open_vacancy in service.list_open_vacancies(today):
        print(f"- {open_vacancy.title} at {open_vacancy.company.name}")

    application = candidate.apply_to(vacancy, today)
    print(f"\n{candidate.name} applied for {vacancy.title}.")
    print(f"Application status: {application.status.name}")

    recruiter.review_application(application, ApplicationStatus.UNDER_REVIEW)
    print(f"After recruiter review: {application.status.name}")

    print(f"Profile skills: {', '.join(candidate.profile.skills)}")
    print(f"Applications stored for the vacancy: {len(vacancy.applications)}")

    try:
        candidate.apply_to(vacancy, today)
    except ValueError as error:
        print(f"\nDuplicate application blocked: {error}")


if __name__ == "__main__":
    main()
