"""Starts the WorkLink graphical interface."""

from tkinter import Tk

from services import WorklinkService
from ui.main_window import MainWindow


def main():
    service = WorklinkService()
    initial_admin = service.create_initial_admin(
        "Administrador WorkLink", "admin@worklink.com"
    )

    root = Tk()
    MainWindow(root, service, initial_admin)
    root.mainloop()


if __name__ == "__main__":
    main()
