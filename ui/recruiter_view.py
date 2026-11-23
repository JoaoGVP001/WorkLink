"""Recruiter interface for vacancies and applications."""

from datetime import date, datetime
from tkinter import messagebox, ttk

from enums import VacancyStatus
from ui.theme import APPLICATION_STATUS_LABELS


class RecruiterView(ttk.Frame):
    VACANCY_STATUS_LABELS = {
        VacancyStatus.OPEN: "Aberta",
        VacancyStatus.CLOSED: "Encerrada",
    }

    def __init__(self, parent, service, selected_user):
        super().__init__(parent, style="App.TFrame")
        self.service = service
        self.recruiter = selected_user
        self._vacancy_rows = {}
        self._application_rows = {}
        self._selected_vacancy = None

        self._build_layout()
        self._refresh_vacancies()
        self._refresh_applications()

    def _build_layout(self):
        ttk.Label(
            self, text="Área do recrutador", style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        company_name = (
            self.recruiter.company.name
            if self.recruiter.company is not None
            else "Sem vínculo com empresa"
        )
        ttk.Label(
            self,
            text=f"Empresa: {company_name}",
            style="CardInfo.TLabel",
        ).pack(anchor="w", pady=(0, 8))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        self.vacancies_tab = ttk.Frame(
            self.notebook, style="App.TFrame", padding=10
        )
        self.applications_tab = ttk.Frame(
            self.notebook, style="App.TFrame", padding=10
        )
        self.notebook.add(self.vacancies_tab, text="Vagas")
        self.notebook.add(self.applications_tab, text="Candidaturas")

        self._build_vacancies_tab()
        self._build_applications_tab()

    def _build_vacancies_tab(self):
        tab = self.vacancies_tab
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=2)
        tab.rowconfigure(0, weight=1)

        form = ttk.Frame(tab, style="Card.TFrame", padding=12)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ttk.Label(form, text="Título da vaga", style="CardBody.TLabel").pack(
            anchor="w"
        )
        self.vacancy_title = ttk.Entry(form)
        self.vacancy_title.pack(fill="x", pady=(3, 8))

        ttk.Label(form, text="Descrição", style="CardBody.TLabel").pack(
            anchor="w"
        )
        self.vacancy_description = ttk.Entry(form)
        self.vacancy_description.pack(fill="x", pady=(3, 8))

        ttk.Label(
            form, text="Prazo (AAAA-MM-DD)", style="CardBody.TLabel"
        ).pack(anchor="w")
        self.vacancy_deadline = ttk.Entry(form)
        self.vacancy_deadline.pack(fill="x", pady=(3, 10))

        buttons = ttk.Frame(form, style="Card.TFrame")
        buttons.pack(fill="x")
        ttk.Button(
            buttons,
            text="Cadastrar",
            command=self._create_vacancy,
            style="Accent.TButton",
        ).pack(side="left")
        ttk.Button(
            buttons,
            text="Atualizar",
            command=self._update_vacancy,
            style="Secondary.TButton",
        ).pack(side="left", padx=6)
        ttk.Button(
            buttons,
            text="Limpar",
            command=self._clear_vacancy_form,
            style="Secondary.TButton",
        ).pack(side="left")

        listing = ttk.Frame(tab, style="Card.TFrame", padding=12)
        listing.grid(row=0, column=1, sticky="nsew")
        listing.rowconfigure(1, weight=1)
        listing.columnconfigure(0, weight=1)

        ttk.Label(
            listing, text="Vagas da empresa", style="CardBody.TLabel"
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.vacancy_tree = ttk.Treeview(
            listing,
            columns=("deadline", "status", "applications"),
            show="tree headings",
            selectmode="browse",
        )
        self.vacancy_tree.heading("#0", text="Título")
        self.vacancy_tree.heading("deadline", text="Prazo")
        self.vacancy_tree.heading("status", text="Situação")
        self.vacancy_tree.heading("applications", text="Candidaturas")
        self.vacancy_tree.column("#0", width=180)
        self.vacancy_tree.column("deadline", width=110, stretch=False)
        self.vacancy_tree.column("status", width=90, stretch=False)
        self.vacancy_tree.column("applications", width=100, stretch=False)
        self.vacancy_tree.grid(row=1, column=0, sticky="nsew")
        self.vacancy_tree.bind("<<TreeviewSelect>>", self._vacancy_selected)

        vacancy_scroll = ttk.Scrollbar(
            listing, orient="vertical", command=self.vacancy_tree.yview
        )
        vacancy_scroll.grid(row=1, column=1, sticky="ns")
        self.vacancy_tree.configure(yscrollcommand=vacancy_scroll.set)

        controls = ttk.Frame(listing, style="Card.TFrame")
        controls.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(
            controls,
            text="Encerrar",
            command=self._close_vacancy,
            style="Secondary.TButton",
        ).pack(side="left")
        ttk.Button(
            controls,
            text="Excluir",
            command=self._delete_vacancy,
            style="Secondary.TButton",
        ).pack(side="left", padx=8)
        ttk.Button(
            controls,
            text="Atualizar lista",
            command=self._refresh_vacancies,
            style="Secondary.TButton",
        ).pack(side="right")

    def _build_applications_tab(self):
        tab = self.applications_tab
        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)

        panel = ttk.Frame(tab, style="Card.TFrame", padding=12)
        panel.grid(row=0, column=0, sticky="nsew")
        panel.rowconfigure(1, weight=1)
        panel.columnconfigure(0, weight=1)

        ttk.Label(
            panel, text="Candidaturas recebidas", style="CardBody.TLabel"
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.application_tree = ttk.Treeview(
            panel,
            columns=("vacancy", "email", "registered", "status"),
            show="tree headings",
            selectmode="browse",
        )
        self.application_tree.heading("#0", text="Candidato")
        self.application_tree.heading("vacancy", text="Vaga")
        self.application_tree.heading("email", text="E-mail")
        self.application_tree.heading("registered", text="Inscrição")
        self.application_tree.heading("status", text="Situação")
        self.application_tree.column("#0", width=170)
        self.application_tree.column("vacancy", width=150)
        self.application_tree.column("email", width=180)
        self.application_tree.column("registered", width=100, stretch=False)
        self.application_tree.column("status", width=100, stretch=False)
        self.application_tree.grid(row=1, column=0, sticky="nsew")
        self.application_tree.bind(
            "<<TreeviewSelect>>", self._application_selected
        )

        application_scroll = ttk.Scrollbar(
            panel, orient="vertical", command=self.application_tree.yview
        )
        application_scroll.grid(row=1, column=1, sticky="ns")
        self.application_tree.configure(yscrollcommand=application_scroll.set)

        controls = ttk.Frame(panel, style="Card.TFrame")
        controls.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Label(
            controls, text="Nova situação:", style="CardBody.TLabel"
        ).pack(side="left")
        self.application_status = ttk.Combobox(
            controls, state="readonly", width=18
        )
        self.application_status.pack(side="left", padx=(8, 10))
        ttk.Button(
            controls,
            text="Avaliar candidatura",
            command=self._review_application,
            style="Accent.TButton",
        ).pack(side="left")
        ttk.Button(
            controls,
            text="Atualizar",
            command=self._refresh_applications,
            style="Secondary.TButton",
        ).pack(side="right")

    def _refresh_vacancies(self):
        self._clear_vacancy_form()
        for item in self.vacancy_tree.get_children():
            self.vacancy_tree.delete(item)
        self._vacancy_rows.clear()
        if self.recruiter.company is None:
            return

        for index, vacancy in enumerate(self.recruiter.company.vacancies):
            row = str(index)
            self._vacancy_rows[row] = vacancy
            self.vacancy_tree.insert(
                "",
                "end",
                iid=row,
                text=vacancy.title,
                values=(
                    vacancy.deadline.isoformat(),
                    self.VACANCY_STATUS_LABELS[vacancy.status],
                    len(vacancy.applications),
                ),
            )

    def _refresh_applications(self):
        self.application_status["values"] = ()
        self.application_status.set("")
        for item in self.application_tree.get_children():
            self.application_tree.delete(item)
        self._application_rows.clear()
        if self.recruiter.company is None:
            return

        index = 0
        for vacancy in self.recruiter.company.vacancies:
            for application in vacancy.applications:
                row = str(index)
                index += 1
                self._application_rows[row] = application
                candidate = application.candidate
                self.application_tree.insert(
                    "",
                    "end",
                    iid=row,
                    text=f"{candidate.user_id} - {candidate.name}",
                    values=(
                        vacancy.title,
                        candidate.email,
                        application.registered_on.isoformat(),
                        APPLICATION_STATUS_LABELS[application.status],
                    ),
                )

    def _vacancy_selected(self, _event=None):
        selection = self.vacancy_tree.selection()
        if not selection:
            self._selected_vacancy = None
            return
        vacancy = self._vacancy_rows.get(selection[0])
        if vacancy is None:
            return
        self._selected_vacancy = vacancy
        self.vacancy_title.delete(0, "end")
        self.vacancy_title.insert(0, vacancy.title)
        self.vacancy_description.delete(0, "end")
        self.vacancy_description.insert(0, vacancy.description)
        self.vacancy_deadline.delete(0, "end")
        self.vacancy_deadline.insert(0, vacancy.deadline.isoformat())

    def _application_selected(self, _event=None):
        selection = self.application_tree.selection()
        application = self._application_rows.get(selection[0]) if selection else None
        allowed = application.review_statuses if application is not None else ()
        labels = [APPLICATION_STATUS_LABELS[status] for status in allowed]
        self.application_status["values"] = tuple(labels)
        self.application_status.set(labels[0] if labels else "")

    def _create_vacancy(self):
        try:
            deadline = self._parse_deadline()
            vacancy = self.recruiter.create_vacancy(
                self.vacancy_title.get(),
                self.vacancy_description.get(),
                deadline,
                date.today(),
            )
        except (ValueError, PermissionError) as error:
            self._show_error(error)
            return
        self._refresh_vacancies()
        self._refresh_applications()
        messagebox.showinfo(
            "Vaga cadastrada", f"A vaga “{vacancy.title}” foi cadastrada."
        )

    def _update_vacancy(self):
        vacancy = self._selected_vacancy
        if vacancy is None:
            messagebox.showinfo(
                "Atualizar vaga", "Selecione uma vaga na lista."
            )
            return
        try:
            deadline = self._parse_deadline()
            self.recruiter.update_vacancy(
                vacancy,
                self.vacancy_title.get(),
                self.vacancy_description.get(),
                deadline,
                date.today(),
            )
        except (ValueError, PermissionError) as error:
            self._show_error(error)
            return
        self._refresh_vacancies()
        messagebox.showinfo("Vaga atualizada", "Os dados da vaga foram atualizados.")

    def _close_vacancy(self):
        vacancy = self._get_selected_vacancy(
            "Encerrar vaga", "Selecione uma vaga na lista."
        )
        if vacancy is None:
            return
        if not messagebox.askyesno(
            "Encerrar vaga",
            f"Deseja encerrar a vaga “{vacancy.title}”?",
        ):
            return
        try:
            self.recruiter.close_vacancy(vacancy)
        except (ValueError, PermissionError) as error:
            self._show_error(error)
            return
        self._refresh_vacancies()
        self._refresh_applications()
        messagebox.showinfo("Vaga encerrada", "A vaga foi encerrada.")

    def _delete_vacancy(self):
        vacancy = self._get_selected_vacancy(
            "Excluir vaga", "Selecione uma vaga na lista."
        )
        if vacancy is None:
            return
        if not messagebox.askyesno(
            "Excluir vaga",
            f"Deseja excluir permanentemente a vaga “{vacancy.title}”?",
        ):
            return
        try:
            self.recruiter.remove_vacancy(vacancy)
        except (ValueError, PermissionError) as error:
            self._show_error(error)
            return
        self._refresh_vacancies()
        self._refresh_applications()
        messagebox.showinfo("Vaga excluída", "A vaga foi excluída.")

    def _review_application(self):
        selection = self.application_tree.selection()
        if not selection:
            messagebox.showinfo(
                "Avaliar candidatura",
                "Selecione uma candidatura na lista.",
            )
            return
        application = self._application_rows.get(selection[0])
        if application is None:
            return

        label = self.application_status.get()
        new_status = next(
            (
                status
                for status, status_label in APPLICATION_STATUS_LABELS.items()
                if status_label == label
            ),
            None,
        )
        if new_status is None:
            messagebox.showinfo(
                "Avaliar candidatura",
                "Selecione uma nova situação permitida.",
            )
            return
        try:
            self.recruiter.review_application(application, new_status)
        except (ValueError, PermissionError) as error:
            self._show_error(error)
            return
        self._refresh_applications()
        self.application_tree.selection_set(selection[0])
        messagebox.showinfo(
            "Candidatura avaliada",
            "A situação da candidatura foi atualizada.",
        )

    def _get_selected_vacancy(self, title, empty_message):
        vacancy = self._selected_vacancy
        if vacancy is None:
            messagebox.showinfo(title, empty_message)
        return vacancy

    def _clear_vacancy_form(self):
        self._selected_vacancy = None
        self.vacancy_title.delete(0, "end")
        self.vacancy_description.delete(0, "end")
        self.vacancy_deadline.delete(0, "end")
        if self.vacancy_tree.selection():
            self.vacancy_tree.selection_remove(self.vacancy_tree.selection())

    def _parse_deadline(self):
        text = self.vacancy_deadline.get().strip()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Informe o prazo no formato AAAA-MM-DD.")

    @staticmethod
    def _show_error(error):
        messagebox.showerror("Operação não realizada", str(error))
