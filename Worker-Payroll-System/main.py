from tkinter import messagebox

import db
from ui import WorkerPayrollApp


def main() -> None:
    """Start the application after checking the MySQL connection."""
    try:
        db.test_connection()
    except Exception as error:
        messagebox.showerror(
            "Database Connection Error",
            f"{error}\n\nRun database.sql and set your MySQL password in db.py.",
        )
        return

    app = WorkerPayrollApp()
    app.mainloop()


if __name__ == "__main__":
    main()
