from datetime import date
from tkinter import Tk

from enums import UserRole
from services import WorklinkService
from ui.main_window import MainWindow


def create_demo_service():
    service = WorklinkService()
    admin = service.create_initial_admin("Admin Teste", "admin@example.com")
    company = service.create_company(admin, "Empresa Teste", "123")
    recruiter = service.create_privileged_account(
        admin, "João Teste", "joao.teste@example.com", UserRole.RECRUITER
    )
    service.assign_recruiter(admin, recruiter, company)

    today = date.today()
    deadline = date(2027, 1, 31)
    if today > deadline:
        return service

    recruiter.create_vacancy(
        "Estágio em Desenvolvimento",
        "Ajudar a equipe a desenvolver e testar sistemas em Python.",
        deadline,
        today,
    )
    recruiter.create_vacancy(
        "Auxiliar de TI",
        "Ajudar no suporte aos usuários e instalar programas nos computadores.",
        deadline,
        today,
    )
    return service


def main():
    root = Tk()
    MainWindow(root, create_demo_service())
    root.mainloop()


if __name__ == "__main__":
    main()
