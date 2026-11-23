"""Shared colors and styles for the Tkinter screens."""

from tkinter import ttk

from enums import ApplicationStatus


APPLICATION_STATUS_LABELS = {
    ApplicationStatus.SENT: "Enviada",
    ApplicationStatus.UNDER_REVIEW: "Em análise",
    ApplicationStatus.APPROVED: "Aprovada",
    ApplicationStatus.REJECTED: "Rejeitada",
    ApplicationStatus.CANCELLED: "Cancelada",
}


def configure_styles(root):
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    background = "#eef2f7"
    dark_blue = "#1f3b5b"
    blue = "#2d6cdf"

    style.configure("App.TFrame", background=background)
    style.configure("Header.TFrame", background=dark_blue)
    style.configure("Card.TFrame", background="#ffffff")
    style.configure(
        "HeaderTitle.TLabel",
        background=dark_blue,
        foreground="#ffffff",
        font=("TkDefaultFont", 21, "bold"),
    )
    style.configure(
        "HeaderSubtitle.TLabel",
        background=dark_blue,
        foreground="#dbe7f5",
        font=("TkDefaultFont", 10),
    )
    style.configure(
        "CardTitle.TLabel",
        background="#ffffff",
        foreground="#1e293b",
        font=("TkDefaultFont", 16, "bold"),
    )
    style.configure(
        "CardBody.TLabel",
        background="#ffffff",
        foreground="#475569",
        font=("TkDefaultFont", 10),
    )
    style.configure(
        "CardInfo.TLabel",
        background="#ffffff",
        foreground="#64748b",
        font=("TkDefaultFont", 9),
    )
    style.configure(
        "Navigation.TLabel",
        background=background,
        foreground="#334155",
        font=("TkDefaultFont", 10, "bold"),
    )
    style.configure(
        "Accent.TButton",
        background=blue,
        foreground="#ffffff",
        padding=(14, 8),
        font=("TkDefaultFont", 10, "bold"),
        borderwidth=0,
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#2459b8"), ("pressed", "#1e4a99")],
        foreground=[("disabled", "#e2e8f0")],
    )
    style.configure(
        "Secondary.TButton",
        background="#ffffff",
        foreground="#334155",
        padding=(10, 6),
        font=("TkDefaultFont", 10),
    )
    style.map(
        "Secondary.TButton",
        background=[("active", "#e2e8f0"), ("pressed", "#cbd5e1")],
    )
    style.configure(
        "HeaderLink.TButton",
        background=dark_blue,
        foreground="#ffffff",
        bordercolor=dark_blue,
        lightcolor=dark_blue,
        darkcolor=dark_blue,
        padding=(8, 6),
    )
    style.map(
        "HeaderLink.TButton",
        background=[("pressed", "#2c517a"), ("active", "#2f5278")],
    )
    style.configure("User.TCombobox", padding=5)
    style.map(
        "User.TCombobox",
        fieldbackground=[("readonly", "#ffffff")],
    )
    return style
