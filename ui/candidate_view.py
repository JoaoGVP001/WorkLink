from datetime import date
import tkinter as tk
from tkinter import messagebox, ttk

from ui.theme import APPLICATION_STATUS_LABELS


class CandidateView(ttk.Frame):

    def __init__(self, parent, service, selected_user, on_user_created=None):
        super().__init__(parent, style="App.TFrame")
        self.service = service
        self.candidate = selected_user
        self.on_user_created = on_user_created

        if self.candidate is None:
            self.create_registration_form()
        else:
            self.create_main_interface()

    def create_registration_form(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame, text="Cadastrar candidato", style="CardTitle.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        ttk.Label(frame, text="Nome", style="CardBody.TLabel").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.name_entry = ttk.Entry(frame, width=35)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(frame, text="E-mail", style="CardBody.TLabel").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.email_entry = ttk.Entry(frame, width=35)
        self.email_entry.grid(row=2, column=1, pady=5, padx=5)

        ttk.Button(
            frame, text="Cadastrar", command=self.handle_register,
            style="Accent.TButton",
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(12, 0))

    def handle_register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        try:
            candidate = self.service.register_candidate(name, email)
        except ValueError as error:
            messagebox.showerror("Erro de cadastro", str(error))
            return
        messagebox.showinfo("Cadastro concluído", "O candidato foi cadastrado.")
        self.on_user_created(candidate)

    def create_main_interface(self):
        for widget in self.winfo_children():
            widget.destroy()

        ttk.Label(
            self, text="Área do candidato", style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.profile_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.profile_frame, text="Meu Perfil")
        self.init_profile_tab()

        self.vacancies_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.vacancies_frame, text="Vagas Abertas")
        self.init_vacancies_tab()

        self.applications_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.applications_frame, text="Minhas Candidaturas")
        self.init_applications_tab()

    def init_profile_tab(self):
        lbl_frame = ttk.LabelFrame(
            self.profile_frame, text="Atualizar Perfil Profissional", padding=(12, 6)
        )
        lbl_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        lbl_frame.columnconfigure(1, weight=1)

        ttk.Label(lbl_frame, text="Resumo profissional").grid(
            row=0, column=0, sticky="nw", padx=(0, 12), pady=2
        )
        self.summary_text = tk.Text(lbl_frame, width=1, height=3, wrap="word")
        self.summary_text.grid(row=0, column=1, sticky="ew", pady=2)
        self.summary_text.insert("1.0", self.candidate.profile.summary)

        ttk.Label(lbl_frame, text="Formação").grid(
            row=1, column=0, sticky="nw", padx=(0, 12), pady=2
        )
        self.education_text = tk.Text(lbl_frame, width=1, height=2, wrap="word")
        self.education_text.grid(row=1, column=1, sticky="ew", pady=2)
        self.education_text.insert("1.0", self.candidate.profile.education)

        ttk.Label(
            lbl_frame, text="Habilidades\n(separadas por vírgula)"
        ).grid(row=2, column=0, sticky=tk.W, padx=(0, 12), pady=2)
        self.skills_entry = ttk.Entry(lbl_frame)
        self.skills_entry.grid(row=2, column=1, sticky="ew", pady=2)
        self.skills_entry.insert(
            0, ", ".join(self.candidate.profile.skills)
        )

        ttk.Button(
            lbl_frame, text="Salvar Alterações do Perfil", command=self.save_profile
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(8, 0))

    def save_profile(self):
        summary = self.summary_text.get("1.0", tk.END).strip()
        education = self.education_text.get("1.0", tk.END).strip()
        skills_raw = self.skills_entry.get().strip()
        skills = [s.strip() for s in skills_raw.split(",") if s.strip()]

        try:
            self.candidate.update_profile(summary, education, skills)
            messagebox.showinfo("Sucesso", "Perfil profissional atualizado com sucesso!")
        except (ValueError, PermissionError) as e:
            messagebox.showerror("Erro", str(e))

    def init_vacancies_tab(self):
        frame = ttk.Frame(self.vacancies_frame, padding=5)

        columns = ("title", "company", "deadline", "description")
        self.vacancies_tree = ttk.Treeview(
            frame, columns=columns, show="headings", selectmode="browse"
        )
        self.vacancies_tree.heading("title", text="Título")
        self.vacancies_tree.heading("company", text="Empresa")
        self.vacancies_tree.heading("deadline", text="Prazo")
        self.vacancies_tree.heading("description", text="Descrição")

        self.vacancies_tree.column("title", width=160)
        self.vacancies_tree.column("company", width=120)
        self.vacancies_tree.column("deadline", width=90)
        self.vacancies_tree.column("description", width=260)

        scrollbar = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=self.vacancies_tree.yview
        )
        self.vacancies_tree.configure(yscrollcommand=scrollbar.set)

        self.vacancies_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_frame = ttk.Frame(self.vacancies_frame, padding=5)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        ttk.Button(
            btn_frame, text="Atualizar Lista", command=self.load_vacancies
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, text="Candidatar-se à Vaga Selecionada", command=self.apply_vacancy
        ).pack(side=tk.LEFT, padx=5)
        frame.pack(fill=tk.BOTH, expand=True)

        self._vacancies_map = {}
        self.load_vacancies()

    def load_vacancies(self):
        for item in self.vacancies_tree.get_children():
            self.vacancies_tree.delete(item)
        self._vacancies_map.clear()

        today = date.today()
        open_vacancies = self.service.list_open_vacancies(today)
        for v in open_vacancies:
            item_id = self.vacancies_tree.insert(
                "",
                tk.END,
                values=(
                    v.title,
                    v.company.name,
                    v.deadline.strftime("%d/%m/%Y"),
                    v.description,
                ),
            )
            self._vacancies_map[item_id] = v

    def apply_vacancy(self):
        selected = self.vacancies_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma vaga para se candidatar.")
            return

        vacancy = self._vacancies_map.get(selected[0])
        if not vacancy:
            return

        try:
            today = date.today()
            self.candidate.apply_to(vacancy, today)
            messagebox.showinfo("Sucesso", f"Candidatura realizada para a vaga: {vacancy.title}!")
            self.load_applications()
        except (ValueError, PermissionError) as e:
            messagebox.showerror("Erro ao candidatar-se", str(e))

    def init_applications_tab(self):
        frame = ttk.Frame(self.applications_frame, padding=5)

        columns = ("title", "company", "registered_on", "status")
        self.applications_tree = ttk.Treeview(
            frame, columns=columns, show="headings", selectmode="browse"
        )
        self.applications_tree.heading("title", text="Vaga")
        self.applications_tree.heading("company", text="Empresa")
        self.applications_tree.heading("registered_on", text="Data Inscrição")
        self.applications_tree.heading("status", text="Status")

        self.applications_tree.column("title", width=180)
        self.applications_tree.column("company", width=130)
        self.applications_tree.column("registered_on", width=100)
        self.applications_tree.column("status", width=120)

        scrollbar = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=self.applications_tree.yview
        )
        self.applications_tree.configure(yscrollcommand=scrollbar.set)

        self.applications_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_frame = ttk.Frame(self.applications_frame, padding=5)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        ttk.Button(
            btn_frame, text="Atualizar Candidaturas", command=self.load_applications
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, text="Cancelar Candidatura Selecionada", command=self.cancel_application
        ).pack(side=tk.LEFT, padx=5)
        frame.pack(fill=tk.BOTH, expand=True)

        self._applications_map = {}
        self.load_applications()

    def load_applications(self):
        for item in self.applications_tree.get_children():
            self.applications_tree.delete(item)
        self._applications_map.clear()

        try:
            applications = self.candidate.list_applications()
        except PermissionError as error:
            messagebox.showerror("Erro ao consultar candidaturas", str(error))
            return
        for app in applications:
            item_id = self.applications_tree.insert(
                "",
                tk.END,
                values=(
                    app.vacancy.title,
                    app.vacancy.company.name,
                    app.registered_on.strftime("%d/%m/%Y"),
                    APPLICATION_STATUS_LABELS[app.status],
                ),
            )
            self._applications_map[item_id] = app

    def cancel_application(self):
        selected = self.applications_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma candidatura para cancelar.")
            return

        app = self._applications_map.get(selected[0])
        if not app:
            return

        if messagebox.askyesno(
            "Confirmação", "Tem certeza que deseja cancelar esta candidatura?"
        ):
            try:
                self.candidate.cancel_application(app)
                messagebox.showinfo("Sucesso", "Candidatura cancelada com sucesso.")
                self.load_applications()
            except (ValueError, PermissionError) as e:
                messagebox.showerror("Erro ao cancelar", str(e))
