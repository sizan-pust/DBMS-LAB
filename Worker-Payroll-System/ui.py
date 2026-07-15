import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk
import db
class WorkerPayrollApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Worker Payroll System")
        self.geometry("1100x650")
        self.worker_id, self.worker_lookup = None, {}
        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True, padx=10, pady=10)
        self.worker_tab, self.payroll_tab = ttk.Frame(tabs), ttk.Frame(tabs)
        tabs.add(self.worker_tab, text="Worker CRUD")
        tabs.add(self.payroll_tab, text="Payroll")
        self.build_worker_tab()
        self.build_payroll_tab()
        self.refresh_all()
    def run(self, action, success=""):
        try:
            result = action()
            if success:
                messagebox.showinfo("Success", success)
            return result
        except Exception as error:
            messagebox.showerror("Error", str(error))
    def build_worker_tab(self):
        self.worker_tab.columnconfigure(1, weight=1)
        self.worker_tab.rowconfigure(0, weight=1)
        form = ttk.LabelFrame(self.worker_tab, text="Worker Information", padding=10)
        form.grid(row=0, column=0, sticky="ns", padx=8, pady=8)
        table = ttk.Frame(self.worker_tab)
        table.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        table.columnconfigure(0, weight=1)
        table.rowconfigure(1, weight=1)

        self.w = {key: tk.StringVar() for key in
                  ("name", "section", "role", "phone", "email", "salary")}
        fields = [("Worker Name", "name"), ("Work Section", "section"),
                  ("Job Role", "role"), ("Phone", "phone"),
                  ("Email", "email"), ("Base Salary", "salary")]

        for row, (text, key) in enumerate(fields):
            ttk.Label(form, text=text).grid(row=row * 2, column=0, sticky="w")
            ttk.Entry(form, textvariable=self.w[key], width=28).grid(
                row=row * 2 + 1, column=0, pady=(0, 6))

        for col, (text, command) in enumerate([
            ("Add", self.add_worker), ("Update", self.update_worker),
            ("Delete", self.delete_worker), ("Clear", self.clear_worker)
        ]):
            ttk.Button(form, text=text, command=command).grid(
                row=12, column=col, padx=2, pady=8)

        self.search = tk.StringVar()
        search = ttk.Frame(table)
        search.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        search.columnconfigure(0, weight=1)
        ttk.Entry(search, textvariable=self.search).grid(row=0, column=0, sticky="ew")
        ttk.Button(search, text="Search",
                   command=lambda: self.load_workers(self.search.get())).grid(
            row=0, column=1, padx=4)
        ttk.Button(search, text="Show All", command=self.show_all).grid(row=0, column=2)

        cols = ("id", "name", "section", "role", "phone", "email", "salary")
        names = ("ID", "Name", "Section", "Role", "Phone", "Email", "Salary")
        self.worker_tree = ttk.Treeview(table, columns=cols, show="headings")
        self.worker_tree.grid(row=1, column=0, sticky="nsew")
        for col, name in zip(cols, names):
            self.worker_tree.heading(col, text=name)
            self.worker_tree.column(col, width=110, anchor="center")
        scroll = ttk.Scrollbar(table, orient="vertical", command=self.worker_tree.yview)
        scroll.grid(row=1, column=1, sticky="ns")
        self.worker_tree.configure(yscrollcommand=scroll.set)
        self.worker_tree.bind("<<TreeviewSelect>>", self.select_worker)
    def worker_data(self):
        data = [self.w[key].get().strip() for key in
                ("name", "section", "role", "phone", "email", "salary")]
        if not all((data[0], data[1], data[2], data[5])):
            raise ValueError("Name, section, role and salary are required.")
        data[5] = float(data[5])
        if data[5] <= 0:
            raise ValueError("Salary must be greater than zero.")
        data[4] = data[4] or None
        return data
    def add_worker(self):
        if self.run(lambda: db.add_worker(*self.worker_data()),
                    "Worker added.") is not None:
            self.clear_worker()
            self.refresh_all()
    def update_worker(self):
        if not self.worker_id:
            return messagebox.showwarning("Warning", "Select a worker first.")
        self.run(lambda: db.update_worker(self.worker_id, *self.worker_data()),
                 "Worker updated.")
        self.clear_worker()
        self.refresh_all()
    def delete_worker(self):
        if not self.worker_id:
            return messagebox.showwarning("Warning", "Select a worker first.")
        if messagebox.askyesno("Confirm", "Delete selected worker?"):
            self.run(lambda: db.delete_worker(self.worker_id), "Worker deleted.")
            self.clear_worker()
            self.refresh_all()
    def load_workers(self, keyword=""):
        rows = self.run(lambda: db.get_workers(keyword)) or []
        self.worker_tree.delete(*self.worker_tree.get_children())
        for x in rows:
            self.worker_tree.insert("", "end", values=(
                x["worker_id"], x["full_name"], x["work_section"], x["job_role"],
                x["phone"] or "", x["email"] or "", x["base_salary"]))
    def select_worker(self, _=None):
        selected = self.worker_tree.selection()
        if not selected:
            return
        values = self.worker_tree.item(selected[0], "values")
        self.worker_id = int(values[0])
        for key, value in zip(("name", "section", "role", "phone", "email", "salary"),
                              values[1:]):
            self.w[key].set(value)
    def clear_worker(self):
        self.worker_id = None
        for value in self.w.values():
            value.set("")
    def show_all(self):
        self.search.set("")
        self.load_workers()
    def build_payroll_tab(self):
        self.payroll_tab.columnconfigure(1, weight=1)
        self.payroll_tab.rowconfigure(0, weight=1)
        form = ttk.LabelFrame(self.payroll_tab, text="Monthly Payroll", padding=10)
        form.grid(row=0, column=0, sticky="ns", padx=8, pady=8)
        table = ttk.Frame(self.payroll_tab)
        table.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        table.columnconfigure(0, weight=1)
        table.rowconfigure(0, weight=1)
        self.p = {
            "worker": tk.StringVar(),
            "month": tk.StringVar(value=date.today().strftime("%Y-%m")),
            "absent": tk.StringVar(value="0"),
            "bonus": tk.StringVar(value="0"),
            "deduction": tk.StringVar(value="0"),
        }
        self.r = {key: tk.StringVar(value="0.00")
                  for key in ("base", "absence", "net")}

        ttk.Label(form, text="Worker").grid(row=0, column=0, sticky="w")
        self.worker_combo = ttk.Combobox(
            form, textvariable=self.p["worker"], state="readonly", width=28)
        self.worker_combo.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        for row, (text, key) in enumerate([
            ("Salary Month", "month"), ("Absent Days", "absent"),
            ("Overtime / Bonus", "bonus"), ("Other Deduction", "deduction")
        ], start=1):
            ttk.Label(form, text=text).grid(row=row * 2, column=0, sticky="w")
            ttk.Entry(form, textvariable=self.p[key]).grid(
                row=row * 2 + 1, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        for row, (text, key) in enumerate([
            ("Base Salary", "base"), ("Absence Deduction", "absence"),
            ("Net Salary", "net")
        ], start=10):
            ttk.Label(form, text=text).grid(row=row, column=0, sticky="w")
            ttk.Label(form, textvariable=self.r[key]).grid(row=row, column=1, sticky="e")

        ttk.Button(form, text="Calculate", command=self.calculate).grid(
            row=13, column=0, pady=8)
        ttk.Button(form, text="Save", command=self.save_payroll).grid(
            row=13, column=1, pady=8)

        cols = ("id", "worker", "month", "base", "absent",
                "bonus", "absence", "other", "net", "date")
        names = ("ID", "Worker", "Month", "Base", "Absent",
                 "Bonus", "Absence", "Other", "Net", "Date")
        self.payroll_tree = ttk.Treeview(table, columns=cols, show="headings")
        self.payroll_tree.grid(row=0, column=0, sticky="nsew")
        for col, name in zip(cols, names):
            self.payroll_tree.heading(col, text=name)
            self.payroll_tree.column(col, width=90, anchor="center")
    def payroll_data(self):
        label = self.p["worker"].get()
        if label not in self.worker_lookup:
            raise ValueError("Select a worker.")
        return (self.worker_lookup[label], self.p["month"].get().strip(),
                int(self.p["absent"].get() or 0),
                float(self.p["bonus"].get() or 0),
                float(self.p["deduction"].get() or 0))
    def calculate(self):
        worker, _, absent, bonus, deduction = self.payroll_data()
        result = self.run(lambda: db.calculate_payroll(
            worker, absent, bonus, deduction))
        if result:
            self.show_result(result)
    def save_payroll(self):
        result = self.run(lambda: db.save_payroll(*self.payroll_data()),
                          "Payroll saved.")
        if result:
            self.show_result(result)
            self.load_payroll()
    def show_result(self, x):
        self.r["base"].set(f'{float(x["base_salary"]):.2f}')
        self.r["absence"].set(f'{float(x["absence_deduction"]):.2f}')
        self.r["net"].set(f'{float(x["net_salary"]):.2f}')
    def load_worker_choices(self):
        workers = self.run(db.get_workers) or []
        self.worker_lookup = {
            f'{x["worker_id"]} - {x["full_name"]}': x["worker_id"] for x in workers}
        self.worker_combo["values"] = list(self.worker_lookup)
    def load_payroll(self):
        rows = self.run(db.get_payroll_history) or []
        self.payroll_tree.delete(*self.payroll_tree.get_children())
        for x in rows:
            self.payroll_tree.insert("", "end", values=(
                x["payroll_id"], x["full_name"], x["salary_month"],
                x["base_salary"], x["absent_days"], x["overtime_bonus"],
                x["absence_deduction"], x["other_deduction"],
                x["net_salary"], x["payment_date"]))
    def refresh_all(self):
        self.load_workers()
        self.load_worker_choices()
        self.load_payroll()