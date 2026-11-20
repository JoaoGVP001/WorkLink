"""Administrator interface for companies, accounts, and recruiter links."""

from tkinter import messagebox, ttk

from enums import UserRole
from models import Administrator, Recruiter


class AdministratorView(ttk.Frame):
    """Allows an administrator to manage companies and privileged accounts."""

    ROLE_LABELS = {
        UserRole.RECRUITER: "Recrutador",
        UserRole.ADMINISTRATOR: "Administrador",
    }

    def __init__(self, parent, service, selected_user, on_user_created):
        super().__init__(parent, style="App.TFrame")
        self.service = service
        self.administrator = selected_user
        self.on_user_created = on_user_created
        self._user_rows = {}
        self._recruiter_options = {}
        self._company_options = {}

        self._build_layout()
        self._refresh_companies()
        self._refresh_recruiters()
        self._refresh_users()

    def _build_layout(self):
        ttk.Label(
            self, text="Área do administrador", style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        self.companies_tab = ttk.Frame(
            self.notebook, style="App.TFrame", padding=10
        )
        self.accounts_tab = ttk.Frame(
            self.notebook, style="App.TFrame", padding=10
        )
        self.users_tab = ttk.Frame(
            self.notebook, style="App.TFrame", padding=10
        )
        self.notebook.add(self.companies_tab, text="Empresas")
        self.notebook.add(self.accounts_tab, text="Contas e vínculos")
        self.notebook.add(self.users_tab, text="Usuários")

        self._build_companies_tab()
        self._build_accounts_tab()
        self._build_users_tab()

    def _build_companies_tab(self):
        tab = self.companies_tab
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=2)
        tab.rowconfigure(0, weight=1)

        form = ttk.Frame(tab, style="Card.TFrame", padding=12)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(form, text="Nome da empresa", style="CardBody.TLabel").pack(
            anchor="w"
        )
        self.company_name = ttk.Entry(form)
        self.company_name.pack(fill="x", pady=(3, 10))
        ttk.Label(
            form, text="CNPJ / identificador", style="CardBody.TLabel"
        ).pack(anchor="w")
        self.company_tax_id = ttk.Entry(form)
        self.company_tax_id.pack(fill="x", pady=(3, 10))
        ttk.Button(
            form,
            text="Cadastrar empresa",
            command=self._create_company,
            style="Accent.TButton",
        ).pack(anchor="w")

        listing = ttk.Frame(tab, style="Card.TFrame", padding=12)
        listing.grid(row=0, column=1, sticky="nsew")
        ttk.Label(
            listing, text="Empresas cadastradas", style="CardBody.TLabel"
        ).pack(anchor="w", pady=(0, 6))
        self.company_tree = ttk.Treeview(
            listing,
            columns=("tax_id", "recruiters"),
            show="headings",
            height=12,
        )
        self.company_tree.heading("tax_id", text="CNPJ / identificador")
        self.company_tree.heading("recruiters", text="Recrutadores")
        self.company_tree.column("tax_id", width=190)
        self.company_tree.column("recruiters", width=100, stretch=False)
        self.company_tree.pack(fill="both", expand=True)

    def _build_accounts_tab(self):
        tab = self.accounts_tab
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)

        account = ttk.Frame(tab, style="Card.TFrame", padding=12)
        account.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(
            account, text="Cadastrar conta privilegiada", style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 8))
        ttk.Label(account, text="Nome", style="CardBody.TLabel").pack(
            anchor="w"
        )
        self.account_name = ttk.Entry(account)
        self.account_name.pack(fill="x", pady=(3, 8))
        ttk.Label(account, text="E-mail", style="CardBody.TLabel").pack(
            anchor="w"
        )
        self.account_email = ttk.Entry(account)
        self.account_email.pack(fill="x", pady=(3, 8))
        ttk.Label(account, text="Tipo de conta", style="CardBody.TLabel").pack(
            anchor="w"
        )
        self.role_choice = ttk.Combobox(
            account,
            state="readonly",
            values=tuple(self.ROLE_LABELS.values()),
        )
        self.role_choice.pack(fill="x", pady=(3, 8))
        self.role_choice.set(self.ROLE_LABELS[UserRole.RECRUITER])
        ttk.Label(
            account, text="Empresa do recrutador (opcional)", style="CardBody.TLabel"
        ).pack(anchor="w")
        self.new_recruiter_company = ttk.Combobox(account, state="readonly")
        self.new_recruiter_company.pack(fill="x", pady=(3, 10))
        ttk.Button(
            account,
            text="Cadastrar conta",
            command=self._create_privileged_account,
            style="Accent.TButton",
        ).pack(anchor="w")

        link = ttk.Frame(tab, style="Card.TFrame", padding=12)
        link.grid(row=0, column=1, sticky="nsew")
        ttk.Label(
            link, text="Vínculo de recrutador", style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 8))
        ttk.Label(link, text="Recrutador", style="CardBody.TLabel").pack(
            anchor="w"
        )
        self.recruiter_choice = ttk.Combobox(link, state="readonly")
        self.recruiter_choice.pack(fill="x", pady=(3, 8))
        self.recruiter_choice.bind(
            "<<ComboboxSelected>>", self._recruiter_selected
        )
        ttk.Label(link, text="Empresa", style="CardBody.TLabel").pack(
            anchor="w"
        )
        self.link_company_choice = ttk.Combobox(link, state="readonly")
        self.link_company_choice.pack(fill="x", pady=(3, 10))
        ttk.Button(
            link,
            text="Salvar vínculo",
            command=self._assign_recruiter,
            style="Accent.TButton",
        ).pack(anchor="w")
        ttk.Label(
            link,
            text="Escolha “Sem vínculo” para remover a empresa atual.",
            style="CardInfo.TLabel",
            wraplength=300,
        ).pack(anchor="w", pady=(10, 0))

    def _build_users_tab(self):
        tab = self.users_tab
        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)
        panel = ttk.Frame(tab, style="Card.TFrame", padding=12)
        panel.grid(row=0, column=0, sticky="nsew")
        panel.rowconfigure(0, weight=1)
        panel.columnconfigure(0, weight=1)
        self.user_tree = ttk.Treeview(
            panel,
            columns=("email", "role", "state"),
            show="tree headings",
            selectmode="browse",
        )
        self.user_tree.heading("#0", text="Usuário")
        self.user_tree.heading("email", text="E-mail")
        self.user_tree.heading("role", text="Perfil")
        self.user_tree.heading("state", text="Situação")
        self.user_tree.column("#0", width=180)
        self.user_tree.column("email", width=240)
        self.user_tree.column("role", width=130, stretch=False)
        self.user_tree.column("state", width=90, stretch=False)
        self.user_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            panel, orient="vertical", command=self.user_tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.user_tree.configure(yscrollcommand=scrollbar.set)

        controls = ttk.Frame(panel, style="Card.TFrame")
        controls.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(
            controls,
            text="Ativar conta",
            command=lambda: self._set_selected_active(True),
            style="Secondary.TButton",
        ).pack(side="left")
        ttk.Button(
            controls,
            text="Desativar conta",
            command=lambda: self._set_selected_active(False),
            style="Secondary.TButton",
        ).pack(side="left", padx=8)
        ttk.Button(
            controls,
            text="Atualizar lista",
            command=self._refresh_users,
            style="Secondary.TButton",
        ).pack(side="right")

    def _refresh_companies(self):
        for item in self.company_tree.get_children():
            self.company_tree.delete(item)
        for company in self.service.companies:
            self.company_tree.insert(
                "",
                "end",
                values=(company.tax_id, len(company.recruiters)),
                text=company.name,
            )
        self._refresh_company_choices()

    def _refresh_company_choices(self):
        self._company_options.clear()
        labels = ["Sem vínculo"]
        self._company_options["Sem vínculo"] = None
        for index, company in enumerate(self.service.companies):
            label = f"{company.name} ({company.tax_id})"
            if label in self._company_options:
                label = f"{label} [{index + 1}]"
            self._company_options[label] = company
            labels.append(label)
        self.link_company_choice["values"] = tuple(labels)
        self.new_recruiter_company["values"] = tuple(labels[1:])
        if self.link_company_choice.get() not in self._company_options:
            self.link_company_choice.set("Sem vínculo")

    def _refresh_recruiters(self, selected=None):
        self._recruiter_options.clear()
        labels = []
        for recruiter in (
            user for user in self.service.users if isinstance(user, Recruiter)
        ):
            label = f"{recruiter.user_id} - {recruiter.name}"
            self._recruiter_options[label] = recruiter
            labels.append(label)
            if recruiter is selected:
                self.recruiter_choice.set(label)
        self.recruiter_choice["values"] = tuple(labels)
        if selected is None or selected not in self._recruiter_options.values():
            self.recruiter_choice.set("")
            self.link_company_choice.set("Sem vínculo")

    def _refresh_users(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        self._user_rows.clear()
        for index, user in enumerate(self.service.list_users(self.administrator)):
            row = str(index)
            self._user_rows[row] = user
            role = self._role_name(user)
            self.user_tree.insert(
                "",
                "end",
                iid=row,
                text=f"{user.user_id} - {user.name}",
                values=(user.email, role, "Ativa" if user.active else "Inativa"),
            )

    def _create_company(self):
        try:
            self.service.create_company(
                self.administrator,
                self.company_name.get(),
                self.company_tax_id.get(),
            )
        except (ValueError, PermissionError) as error:
            self._show_error(error)
            return
        self.company_name.delete(0, "end")
        self.company_tax_id.delete(0, "end")
        self._refresh_companies()
        messagebox.showinfo("Empresa cadastrada", "A empresa foi cadastrada.")

    def _create_privileged_account(self):
        role = next(
            (
                account_role
                for account_role, label in self.ROLE_LABELS.items()
                if label == self.role_choice.get()
            ),
            None,
        )
        if role is None:
            messagebox.showinfo(
                "Cadastrar conta", "Selecione um tipo de conta válido."
            )
            return
        try:
            user = self.service.create_privileged_account(
                self.administrator,
                self.account_name.get(),
                self.account_email.get(),
                role,
            )
            if isinstance(user, Recruiter):
                company_label = self.new_recruiter_company.get()
                company = self._company_options.get(company_label)
                if company is not None:
                    self.service.assign_recruiter(
                        self.administrator, user, company
                    )
        except (ValueError, PermissionError) as error:
            self._show_error(error)
            return
        self.account_name.delete(0, "end")
        self.account_email.delete(0, "end")
        self.new_recruiter_company.set("")
        self._refresh_recruiters(user if isinstance(user, Recruiter) else None)
        self._refresh_users()
        self.on_user_created(user)
        messagebox.showinfo("Conta cadastrada", "A conta foi cadastrada.")

    def _recruiter_selected(self, _event=None):
        recruiter = self._recruiter_options.get(self.recruiter_choice.get())
        if recruiter is None:
            return
        for label, company in self._company_options.items():
            if company is recruiter.company:
                self.link_company_choice.set(label)
                return

    def _assign_recruiter(self):
        recruiter = self._recruiter_options.get(self.recruiter_choice.get())
        if recruiter is None:
            messagebox.showinfo(
                "Vínculo de recrutador", "Selecione um recrutador."
            )
            return
        company = self._company_options.get(self.link_company_choice.get())
        try:
            self.service.assign_recruiter(
                self.administrator, recruiter, company
            )
        except (ValueError, PermissionError) as error:
            self._show_error(error)
            return
        self._refresh_companies()
        self._refresh_recruiters(recruiter)
        messagebox.showinfo("Vínculo atualizado", "O vínculo foi atualizado.")

    def _set_selected_active(self, active):
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showinfo(
                "Gerenciar conta", "Selecione um usuário da lista."
            )
            return
        user = self._user_rows.get(selection[0])
        if user is None:
            return
        try:
            self.service.set_account_active(
                self.administrator, user, active
            )
        except (ValueError, PermissionError) as error:
            self._show_error(error)
            return
        self._refresh_users()
        self._refresh_recruiters(
            user if isinstance(user, Recruiter) else None
        )

    @classmethod
    def _role_name(cls, user):
        if isinstance(user, Recruiter):
            return cls.ROLE_LABELS[UserRole.RECRUITER]
        if isinstance(user, Administrator):
            return cls.ROLE_LABELS[UserRole.ADMINISTRATOR]
        return "Candidato"

    @staticmethod
    def _show_error(error):
        messagebox.showerror("Operação não realizada", str(error))
