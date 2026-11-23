"""Main window and navigation for the WorkLink demo application."""

import tkinter as tk
from tkinter import messagebox, ttk

from models import Administrator, Candidate, Recruiter
from ui.admin_view import AdministratorView
from ui.candidate_view import CandidateView
from ui.recruiter_view import RecruiterView
from ui.theme import configure_styles


class MainWindow:
    VIEW_DETAILS = {
        Candidate: ("Candidato", CandidateView),
        Recruiter: ("Recrutador", RecruiterView),
        Administrator: ("Administrador", AdministratorView),
    }

    def __init__(self, root, service, initial_user=None):
        self.root = root
        self.service = service
        self.current_user = initial_user
        self._user_options = {}

        configure_styles(self.root)
        self.root.title("WorkLink - Sistema de Vagas")
        self.root.geometry("820x560")
        self.root.minsize(680, 540)
        self.root.configure(bg="#eef2f7")

        self._build_layout()
        self.refresh_users(initial_user)
        self.show_home()

    def _build_layout(self):
        self.container = ttk.Frame(self.root, style="App.TFrame")
        self.container.pack(fill="both", expand=True)

        self.header = ttk.Frame(
            self.container, style="Header.TFrame", padding=(22, 16)
        )
        self.header.pack(fill="x")

        ttk.Label(
            self.header,
            text="WorkLink",
            style="HeaderTitle.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            self.header,
            text="Sistema de divulgação de vagas e candidaturas",
            style="HeaderSubtitle.TLabel",
        ).pack(anchor="w", pady=(2, 10))

        self.navigation = ttk.Frame(
            self.container, style="App.TFrame", padding=(22, 12)
        )
        self.navigation.pack(fill="x")

        ttk.Label(
            self.navigation,
            text="Usuário da demonstração:",
            style="Navigation.TLabel",
        ).pack(side="left")
        self.user_choice = tk.StringVar()
        self.user_menu = ttk.Combobox(
            self.navigation,
            textvariable=self.user_choice,
            state="readonly",
            width=34,
            style="User.TCombobox",
        )
        self.user_menu.pack(side="left", padx=(8, 10))
        self.user_choice.trace_add("write", self._selection_changed)

        ttk.Button(
            self.navigation,
            text="Atualizar usuários",
            command=self.refresh_users,
            style="Secondary.TButton",
        ).pack(side="left")
        ttk.Button(
            self.navigation,
            text="Início",
            command=self.show_home,
            style="Secondary.TButton",
        ).pack(side="right")

        self.content = ttk.Frame(
            self.container, style="App.TFrame", padding=(22, 10, 22, 22)
        )
        self.content.pack(fill="both", expand=True)

    def refresh_users(self, selected_user=None):
        if selected_user is not None:
            self.current_user = selected_user

        self._user_options.clear()
        for user in self.service.users:
            role = self._role_name(user)
            state = "ativo" if user.active else "inativo"
            label = f"{user.user_id} - {user.name} ({role}, {state})"
            self._user_options[label] = user

        selected_label = None
        for label, user in self._user_options.items():
            if user is self.current_user:
                selected_label = label

        self.user_menu["values"] = tuple(self._user_options)

        if selected_label is None and self._user_options:
            selected_label = next(iter(self._user_options))
            self.current_user = self._user_options[selected_label]

        if selected_label is None:
            self.current_user = None
            self.user_choice.set("Nenhum usuário cadastrado")
        else:
            self.user_choice.set(selected_label)

    def show_home(self):
        self._clear_content()
        card = ttk.Frame(self.content, style="Card.TFrame", padding=24)
        card.pack(fill="both", expand=True)

        ttk.Label(
            card,
            text="Demonstração do sistema",
            style="CardTitle.TLabel",
        ).pack(anchor="w", pady=(0, 12))

        if self.current_user is None:
            ttk.Label(
                card,
                text="Cadastre um candidato ou atualize a lista de usuários.",
                wraplength=620,
                justify="left",
                style="CardBody.TLabel",
            ).pack(anchor="w", pady=(0, 12))
        else:
            role = self._role_name(self.current_user)
            state = "Ativa" if self.current_user.active else "Inativa"
            ttk.Label(
                card,
                text=f"Perfil selecionado: {self.current_user.name}",
                style="CardBody.TLabel",
            ).pack(anchor="w", pady=(4, 6))
            ttk.Label(
                card,
                text=f"Tipo de perfil: {role}",
                style="CardBody.TLabel",
            ).pack(anchor="w", pady=4)
            ttk.Label(
                card,
                text=f"Situação da conta: {state}",
                style="CardBody.TLabel",
            ).pack(anchor="w", pady=4)

            ttk.Button(
                card,
                text=f"Abrir área de {role.lower()}",
                command=self.open_selected_area,
                style="Accent.TButton",
            ).pack(anchor="w", pady=(18, 8))

        ttk.Button(
            card,
            text="Cadastrar candidato",
            command=self.open_candidate_registration,
            style="Secondary.TButton",
        ).pack(anchor="w", pady=4)

        ttk.Label(
            card,
            text=(
                "A seleção de usuário serve para demonstrar os perfis. "
                "Não é um sistema de login. Os dados ficam na memória e "
                "são apagados quando o programa é fechado."
            ),
            wraplength=620,
            justify="left",
            style="CardInfo.TLabel",
        ).pack(anchor="w", pady=(22, 0))

    def open_selected_area(self):
        if self.current_user is None:
            messagebox.showinfo(
                "WorkLink", "Selecione um usuário para abrir a área."
            )
            return

        try:
            self.current_user.ensure_active()
        except PermissionError:
            messagebox.showerror("WorkLink", "Essa conta está inativa.")
            return

        _, view_class = self.VIEW_DETAILS[type(self.current_user)]
        self._open_profile_view(view_class, self.current_user)

    def open_candidate_registration(self):
        self._open_profile_view(CandidateView, None)

    def _open_profile_view(self, view_class, user):
        self._clear_content()
        view = view_class(self.content, self.service, user, self.refresh_users)
        view.pack(fill="both", expand=True)

    def _selection_changed(self, *_args):
        label = self.user_choice.get()
        selected_user = self._user_options.get(label)
        if selected_user is not None and selected_user is not self.current_user:
            self.current_user = selected_user
            self.show_home()

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    @staticmethod
    def _role_name(user):
        for user_type, details in MainWindow.VIEW_DETAILS.items():
            if isinstance(user, user_type):
                return details[0]
        return "Usuário"
