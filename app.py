import tkinter as tk
from tkinter import messagebox
from project import Project


class TodoApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Todo List")
        self.project = Project("My Project")

        self._build_ui()

    def _build_ui(self) -> None:
        # ---- Input frame ----
        input_frame = tk.LabelFrame(self.root, text="New Task", padx=8, pady=8)
        input_frame.pack(fill="x", padx=10, pady=8)

        labels = ["Title", "Description", "Label", "Due Date (YYYY-MM-DD)"]
        self.entries: dict[str, tk.Entry] = {}

        for row, name in enumerate(labels):
            tk.Label(input_frame, text=name + ":").grid(
                row=row, column=0, sticky="w", pady=2
            )
            entry = tk.Entry(input_frame, width=35)
            entry.grid(row=row, column=1, sticky="w", padx=6, pady=2)
            self.entries[name] = entry

        # Status dropdown
        tk.Label(input_frame, text="Status:").grid(
            row=len(labels), column=0, sticky="w", pady=2
        )
        self.status_var = tk.StringVar(value="todo")
        status_menu = tk.OptionMenu(
            input_frame,
            self.status_var,
            "todo",
            "in-progress",
            "done",
            "cancelled",
        )
        status_menu.grid(row=len(labels), column=1, sticky="w", padx=6)

        # ---- Button frame ----
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=4)

        tk.Button(btn_frame, text="Add Task", width=14, command=self._add_end).pack(
            side="left", padx=4
        )
        tk.Button(btn_frame, text="Toggle Done", width=12, command=self._mark_done).pack(
            side="left", padx=4
        )

        # ---- Task list ----
        list_frame = tk.LabelFrame(self.root, text="Tasks", padx=8, pady=8)
        list_frame.pack(fill="both", expand=True, padx=10, pady=8)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.listbox = tk.Listbox(
            list_frame,
            width=70,
            height=14,
            yscrollcommand=scrollbar.set,
            font=("Courier", 10),
        )
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)

        self.status_bar = tk.Label(
            self.root, text="0 tasks", anchor="w", relief="sunken"
        )
        self.status_bar.pack(fill="x", padx=10, pady=(0, 6))

    def _get_inputs(self) -> dict | None:
        title = self.entries["Title"].get().strip()
        if not title:
            messagebox.showwarning("Missing title", "Please enter a task title.")
            return None
        return {
            "title": title,
            "description": self.entries["Description"].get().strip(),
            "label": self.entries["Label"].get().strip() or "general",
            "due_date": self.entries["Due Date (YYYY-MM-DD)"].get().strip() or None,
            "status": self.status_var.get(),
        }

    def _clear_inputs(self) -> None:
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.status_var.set("todo")

    def _refresh_list(self) -> None:
        self.listbox.delete(0, tk.END)
        for task in self.project.get_all_tasks():
            due = task.due_date or "—"
            line = f"[{task.status:<11}] {due:<12}  {task.title:<28} ({task.label})"
            self.listbox.insert(tk.END, line)
        self.status_bar.config(text=f"{len(self.project)} task(s)")

    def _selected_title(self) -> str | None:
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "No selection", "Please select a task from the list."
            )
            return None
        tasks = self.project.get_all_tasks()
        return tasks[selection[0]].title

    def _add_end(self) -> None:
        data = self._get_inputs()
        if data is None:
            return
        try:
            self.project.add_task(**data)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self._clear_inputs()
        self._refresh_list()

    def _add_beginning(self) -> None:
        data = self._get_inputs()
        if data is None:
            return
        try:
            self.project.add_task_at_beginning(**data)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self._clear_inputs()
        self._refresh_list()

    def _mark_done(self) -> None:
        title = self._selected_title()
        if title is None:
            return
        self.project.toggle_done(title)
        self._refresh_list()