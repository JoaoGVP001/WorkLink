from datetime import date
import tkinter as tk
from tkinter import messagebox, ttk

from models import Candidate


class CandidateView(tk.Frame):

    def __init__(self, parent, service, candidate=None):
        super().__init__(parent)
        self.service = service
        self.candidate = candidate

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        if not self.candidate:
            self.create_auth_widgets()
        else:
            self.create_main_interface()

    def create_auth_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        frame = ttk.LabelFrame(self, text="Identificação do Candidato", padding=20)
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(frame, width=35)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(frame, text="E-mail:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(frame, width=35)
        self.email_entry.grid(row=1, column=1, pady=5, padx=5)

        btn_register = ttk.Button(
            frame, text="Cadastrar Novo Candidato", command=self.handle_register
        )
        btn_register.grid(row=2, column=0, columnspan=2, pady=15)

        existing_candidates = [
            u for u in self.service.users if isinstance(u, Candidate)
        ]
        if existing_candidates:
            ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
                row=3, column=0, columnspan=2, sticky="ew", pady=15
            )
            ttk.Label(frame, text="Ou selecione um candidato existente:").grid(
                row=4, column=0, columnspan=2, sticky=tk.W, pady=5
            )

            self.candidate_combobox = ttk.Combobox(
                frame,
                values=[f"{c.name} ({c.email})" for c in existing_candidates],
                state="readonly",
                width=40,
            )
            self.candidate_combobox.grid(row=5, column=0, columnspan=2, pady=5)
            self._existing_candidates = existing_candidates

            btn_select = ttk.Button(
                frame, text="Selecionar Candidato", command=self.handle_select_existing
            )
            btn_select.grid(row=6, column=0, columnspan=2, pady=10)

    def handle_register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        try:
            self.candidate = self.service.register_candidate(name, email)
            messagebox.showinfo(
                "Sucesso", f"Candidato {self.candidate.name} cadastrado com sucesso!"
            )
            self.create_main_interface()
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", str(e))

    def handle_select_existing(self):
        selection = self.candidate_combobox.current()
        if selection >= 0:
            self.candidate = self._existing_candidates[selection]
            self.create_main_interface()
        else:
            messagebox.showwarning("Aviso", "Selecione um candidato válido na lista.")

    def create_main_interface(self):
        for widget in self.winfo_children():
            widget.destroy()

        top_frame = ttk.Frame(self, padding=10)
        top_frame.pack(fill=tk.X)

        ttk.Label(
            top_frame,
            text=f"Candidato: {self.candidate.name} ({self.candidate.email})",
            font=("Arial", 11, "bold"),
        ).pack(side=tk.LEFT)

        ttk.Button(
            top_frame, text="Trocar / Sair", command=self.create_auth_widgets
        ).pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

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
            self.profile_frame, text="Atualizar Perfil Profissional", padding=15
        )
        lbl_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(lbl_frame, text="Resumo Profissional:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.summary_text = tk.Text(lbl_frame, width=55, height=4)
        self.summary_text.grid(row=1, column=0, columnspan=2, pady=5)
        self.summary_text.insert("1.0", self.candidate.profile.summary)

        ttk.Label(lbl_frame, text="Educação:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.education_text = tk.Text(lbl_frame, width=55, height=3)
        self.education_text.grid(row=3, column=0, columnspan=2, pady=5)
        self.education_text.insert("1.0", self.candidate.profile.education)

        ttk.Label(
            lbl_frame, text="Habilidades (separadas por vírgula):"
        ).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.skills_entry = ttk.Entry(lbl_frame, width=57)
        self.skills_entry.grid(row=5, column=0, columnspan=2, pady=5)
        self.skills_entry.insert(
            0, ", ".join(self.candidate.profile.skills)
        )

        ttk.Button(
            lbl_frame, text="Salvar Alterações do Perfil", command=self.save_profile
        ).grid(row=6, column=0, columnspan=2, pady=15)

    def save_profile(self):
        summary = self.summary_text.get("1.0", tk.END).strip()
        education = self.education_text.get("1.0", tk.END).strip()
        skills_raw = self.skills_entry.get().strip()
        skills = [s.strip() for s in skills_raw.split(",") if s.strip()]

        try:
            self.candidate.update_profile(summary, education, skills)
            messagebox.showinfo("Sucesso", "Perfil profissional atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def init_vacancies_tab(self):
        frame = ttk.Frame(self.vacancies_frame, padding=5)
        frame.pack(fill=tk.BOTH, expand=True)

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
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            btn_frame, text="Atualizar Lista", command=self.load_vacancies
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, text="Candidatar-se à Vaga Selecionada", command=self.apply_vacancy
        ).pack(side=tk.LEFT, padx=5)

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
        except Exception as e:
            messagebox.showerror("Erro ao candidatar-se", str(e))

    def init_applications_tab(self):
        frame = ttk.Frame(self.applications_frame, padding=5)
        frame.pack(fill=tk.BOTH, expand=True)

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
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(
            btn_frame, text="Atualizar Candidaturas", command=self.load_applications
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, text="Cancelar Candidatura Selecionada", command=self.cancel_application
        ).pack(side=tk.LEFT, padx=5)

        self._applications_map = {}
        self.load_applications()

    def load_applications(self):
        for item in self.applications_tree.get_children():
            self.applications_tree.delete(item)
        self._applications_map.clear()

        try:
            applications = self.candidate.list_applications()
            for app in applications:
                status_name = app.status.name
                item_id = self.applications_tree.insert(
                    "",
                    tk.END,
                    values=(
                        app.vacancy.title,
                        app.vacancy.company.name,
                        app.registered_on.strftime("%d/%m/%Y"),
                        status_name,
                    ),
                )
                self._applications_map[item_id] = app
        except Exception:
            pass

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
            except Exception as e:
                messagebox.showerror("Erro ao cancelar", str(e))