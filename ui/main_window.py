from datetime import date
from tkinter import messagebox, ttk

from models import Administrator, Candidate, Recruiter
from ui.admin_view import AdministratorView
from ui.candidate_view import CandidateView
from ui.recruiter_view import RecruiterView
from ui.theme import configure_styles
from ui.vacancies_view import VacanciesView


class MainWindow:
    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.candidate = None

        configure_styles(root)
        root.title("WorkLink - Sistema de Vagas")
        root.geometry("900x590")
        root.minsize(680, 540)
        self._build_layout()
        self.show_home()

    def _build_layout(self):
        container = ttk.Frame(self.root, style="App.TFrame")
        container.pack(fill="both", expand=True)

        header = ttk.Frame(container, style="Header.TFrame", padding=(20, 14))
        header.pack(fill="x")
        brand = ttk.Frame(header, style="Header.TFrame")
        brand.pack(side="left")
        ttk.Label(brand, text="WorkLink", style="HeaderTitle.TLabel").pack(anchor="w")
        ttk.Label(
            brand, text="Vagas de emprego e estágio", style="HeaderSubtitle.TLabel"
        ).pack(anchor="w")

        actions = ttk.Frame(header, style="Header.TFrame")
        actions.pack(side="right")
        self.home_button = ttk.Button(
            actions, text="Voltar às vagas", style="HeaderLink.TButton", command=self.show_home
        )
        self.home_button.grid(row=0, column=0, padx=(0, 4))
        ttk.Button(
            actions, text="Área do candidato", style="HeaderLink.TButton",
            command=self.show_candidate_picker,
        ).grid(row=0, column=1, padx=(0, 4))
        ttk.Button(
            actions, text="Área da empresa", style="HeaderLink.TButton",
            command=self.show_company_picker,
        ).grid(row=0, column=2)

        self.content = ttk.Frame(container, style="App.TFrame", padding=(20, 16))
        self.content.pack(fill="both", expand=True)

    def show_home(self):
        self._clear_content()
        self.home_button.grid_remove()
        view = VacanciesView(self.content, self.service, self.start_application)
        view.pack(fill="both", expand=True)

    def show_candidate_picker(self, vacancy=None):
        if vacancy is None:
            card = self._card("Área do candidato")
            action = "Abrir área"
        else:
            card = self._card("Selecione uma conta")
            ttk.Label(
                card, text=f"Vaga selecionada: {vacancy.title}", style="CardBody.TLabel",
                wraplength=550,
            ).pack(anchor="w", pady=(0, 12))
            action = "Continuar"

        candidates = [user for user in self.service.users if isinstance(user, Candidate)]
        if candidates:
            self._account_picker(
                card, candidates, action,
                lambda candidate: self._select_candidate(candidate, vacancy),
                selected_user=self.candidate,
            )

        ttk.Button(
            card,
            text="Cadastrar candidato",
            style="Secondary.TButton" if candidates else "Accent.TButton",
            command=lambda: self._show_candidate_registration(vacancy),
        ).pack(anchor="w", pady=(12, 0))

    def _show_candidate_registration(self, vacancy):
        self._clear_content()
        view = CandidateView(
            self.content, self.service, None,
            lambda candidate: self._select_candidate(candidate, vacancy),
        )
        view.pack(fill="both", expand=True)

    def _select_candidate(self, candidate, vacancy):
        if not self._ensure_active(candidate):
            return

        self.candidate = candidate
        if vacancy is None:
            self._show_candidate_area()
        else:
            self._show_confirmation(candidate, vacancy)

    def _show_candidate_area(self, show_applications=False):
        self._clear_content()
        view = CandidateView(self.content, self.service, self.candidate)
        view.pack(fill="both", expand=True)
        if show_applications:
            view.notebook.select(view.applications_frame)

    def start_application(self, vacancy):
        if self.candidate is not None and self.candidate.active:
            self._show_confirmation(self.candidate, vacancy)
        else:
            self.show_candidate_picker(vacancy)

    def _show_confirmation(self, candidate, vacancy):
        card = self._card("Confirmar candidatura")
        for text in (
            vacancy.title,
            vacancy.company.name,
            f"Candidato: {candidate.name}",
        ):
            ttk.Label(
                card, text=text, style="CardBody.TLabel", wraplength=550
            ).pack(anchor="w", pady=(0, 6))

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(anchor="w", pady=(10, 0))
        ttk.Button(
            actions, text="Enviar candidatura", style="Accent.TButton",
            command=lambda: self._confirm_application(candidate, vacancy),
        ).pack(side="left")
        ttk.Button(
            actions, text="Cancelar", style="Secondary.TButton", command=self.show_home
        ).pack(side="left", padx=(8, 0))

    def _confirm_application(self, candidate, vacancy):
        try:
            candidate.apply_to(vacancy, date.today())
        except (PermissionError, ValueError) as error:
            messagebox.showerror("Candidatura não enviada", str(error), parent=self.root)
            return

        self._show_candidate_area(show_applications=True)
        messagebox.showinfo(
            "Candidatura enviada", f"Sua candidatura para {vacancy.title} foi enviada.",
            parent=self.root,
        )

    def show_company_picker(self):
        card = self._card("Área da empresa")
        users = [
            user for user in self.service.users if isinstance(user, (Administrator, Recruiter))
        ]
        self._account_picker(card, users, "Abrir área", self._show_company_area)
        ttk.Label(
            card, text="Escolha uma conta de demonstração para abrir a área.",
            style="CardInfo.TLabel",
        ).pack(anchor="w", pady=(12, 0))

    def _show_company_area(self, user):
        if not self._ensure_active(user):
            return
        self._clear_content()
        view_class = AdministratorView if isinstance(user, Administrator) else RecruiterView
        view_class(self.content, self.service, user).pack(fill="both", expand=True)

    def _account_picker(self, card, users, action, on_select, selected_user=None):
        if not users:
            ttk.Label(card, text="Nenhuma conta disponível.", style="CardBody.TLabel").pack(
                anchor="w"
            )
            return

        picker = ttk.Combobox(
            card,
            values=[self._account_label(user) for user in users],
            state="readonly",
            width=42,
            style="User.TCombobox",
        )
        picker.current(users.index(selected_user) if selected_user in users else 0)
        picker.pack(anchor="w", pady=(0, 10))
        ttk.Button(
            card, text=action, style="Accent.TButton",
            command=lambda: on_select(users[picker.current()]),
        ).pack(anchor="w")

    def _card(self, title):
        self._clear_content()
        card = ttk.Frame(self.content, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(
            anchor="w", pady=(0, 12)
        )
        return card

    def _clear_content(self):
        self.home_button.grid()
        for child in self.content.winfo_children():
            child.destroy()

    def _ensure_active(self, user):
        try:
            user.ensure_active()
        except PermissionError:
            messagebox.showerror("Conta inativa", "Essa conta está inativa.", parent=self.root)
            return False
        return True

    @staticmethod
    def _account_label(user):
        roles = {
            Administrator: "Administrador",
            Recruiter: "Recrutador",
            Candidate: "Candidato",
        }
        role = roles[type(user)]
        state = "" if user.active else " • inativo"
        return f"{user.name} ({role}{state}) · {user.user_id}"
