import tkinter as tk
from datetime import date
from tkinter import ttk


class VacanciesView(ttk.Frame):
    def __init__(self, parent, service, on_apply):
        super().__init__(parent, style="App.TFrame")
        self.on_apply = on_apply
        self.vacancies = {}
        self._build_layout()

        for vacancy in service.list_open_vacancies(date.today()):
            row = self.table.insert(
                "",
                "end",
                values=(vacancy.title, vacancy.company.name, vacancy.deadline.strftime("%d/%m/%Y")),
            )
            self.vacancies[row] = vacancy

        if self.vacancies:
            self.table.selection_set(next(iter(self.vacancies)))
        self._update_details()

    def _build_layout(self):
        self.columnconfigure(0, weight=3, uniform="panels")
        self.columnconfigure(1, weight=2, uniform="panels")
        self.rowconfigure(0, weight=1)

        listing = ttk.Frame(self, style="Card.TFrame", padding=14)
        listing.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        listing.columnconfigure(0, weight=1)
        listing.rowconfigure(1, weight=1)
        ttk.Label(listing, text="Vagas abertas", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )
        self.table = ttk.Treeview(
            listing,
            columns=("title", "company", "deadline"),
            show="headings",
            selectmode="browse",
            height=7,
        )
        for column, label, width in (
            ("title", "Vaga", 172),
            ("company", "Empresa", 130),
            ("deadline", "Prazo", 92),
        ):
            self.table.heading(column, text=label, anchor="w")
            self.table.column(column, width=width, minwidth=45, stretch=column != "deadline")
        self.table.grid(row=1, column=0, sticky="nsew")
        self._add_scrollbar(listing, self.table, 1)
        self.table.bind("<<TreeviewSelect>>", self._update_details)

        details = ttk.Frame(self, style="Card.TFrame", padding=14)
        details.grid(row=0, column=1, sticky="nsew")
        details.columnconfigure(0, weight=1)
        details.rowconfigure(2, weight=1)

        self.title = ttk.Label(details, style="CardTitle.TLabel", wraplength=205)
        self.title.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.deadline = ttk.Label(details, style="CardBody.TLabel", wraplength=205)
        self.deadline.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 10))
        details.bind("<Configure>", self._resize_details)

        self.description = tk.Text(
            details, width=1, height=4, wrap="word", font="TkDefaultFont",
            background="white", foreground="#334155", relief="flat",
            highlightthickness=0, padx=0, pady=0, cursor="arrow",
        )
        self.description.grid(row=2, column=0, sticky="nsew")
        self._add_scrollbar(details, self.description, 2)

        self.apply_button = ttk.Button(
            details, text="Quero me candidatar", style="Accent.TButton", command=self._apply
        )
        self.apply_button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 0))

    def _resize_details(self, event):
        width = max(1, event.width - 28)
        self.title.configure(wraplength=width)
        self.deadline.configure(wraplength=width)

    @staticmethod
    def _add_scrollbar(parent, widget, row):
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=widget.yview)
        scrollbar.grid(row=row, column=1, sticky="ns")
        widget.configure(yscrollcommand=scrollbar.set)

    def _selected_vacancy(self):
        selection = self.table.selection()
        return self.vacancies.get(selection[0]) if selection else None

    def _update_details(self, _event=None):
        vacancy = self._selected_vacancy()
        if vacancy is None:
            heading = "Selecione uma vaga" if self.vacancies else "Nenhuma vaga aberta"
            subtitle = ""
            text = "" if self.vacancies else "Nenhuma vaga aberta no momento."
        else:
            heading = vacancy.title
            subtitle = f"{vacancy.company.name}\nPrazo: {vacancy.deadline:%d/%m/%Y}"
            text = vacancy.description

        self.title.configure(text=heading)
        self.deadline.configure(text=subtitle)
        self.description.configure(state="normal")
        self.description.delete("1.0", "end")
        self.description.insert("1.0", text)
        self.description.configure(state="disabled")
        self.apply_button.configure(state="normal" if vacancy is not None else "disabled")

    def _apply(self):
        vacancy = self._selected_vacancy()
        if vacancy is not None:
            self.on_apply(vacancy)
