from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TodoNode:
    """Represents a single task and acts as a node in the linked list."""

    title: str
    description: str = ""
    label: str = "general"
    due_date: str | None = None
    status: str = "todo"
    next: TodoNode | None = field(default=None, repr=False)

    def __str__(self) -> str:
        due = self.due_date if self.due_date else "no due date"
        return (
            f"TodoNode(title={self.title!r}, status={self.status!r}, "
            f"label={self.label!r}, due={due})"
        )


class Project:
    """
    A project that holds tasks as a singly linked list.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.head: TodoNode | None = None
        self.size: int = 0

    def _make_node(
        self,
        title: str,
        description: str,
        label: str,
        due_date: str | None,
        status: str,
    ) -> TodoNode:
        valid_statuses = {"todo", "in-progress", "done", "cancelled"}
        if status not in valid_statuses:
            raise ValueError(f"status must be one of {valid_statuses}, got {status!r}")
        return TodoNode(
            title=title,
            description=description,
            label=label,
            due_date=due_date,
            status=status,
        )

    def add_task(
        self,
        title: str,
        description: str = "",
        label: str = "general",
        due_date: str | None = None,
        status: str = "todo",
    ) -> None:
        """Append a new task at the END of the list. O(n)."""
        new_node = self._make_node(title, description, label, due_date, status)

        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

        self.size += 1

    def add_task_at_beginning(
        self,
        title: str,
        description: str = "",
        label: str = "general",
        due_date: str | None = None,
        status: str = "todo",
    ) -> None:
        new_node = self._make_node(title, description, label, due_date, status)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def get_all_tasks(self) -> list[TodoNode]:
        tasks: list[TodoNode] = []
        current = self.head
        while current is not None:
            tasks.append(current)
            current = current.next
        return tasks

    def find_task_by_title(self, title: str) -> TodoNode | None:
        current = self.head
        while current is not None:
            if current.title == title:
                return current
            current = current.next
        return None

    def mark_done(self, title: str) -> bool:
        node = self.find_task_by_title(title)
        if node is None:
            return False
        node.status = "done"
        return True

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        lines: list[str] = [f'Project: "{self.name}"']

        if self.head is None:
            lines.append("  (no tasks yet)")
            return "\n".join(lines)

        for index, task in enumerate(self.get_all_tasks(), start=1):
            status_col  = f"[{task.status}]"
            due_col     = task.due_date or ""
            title_col   = task.title
            label_col   = f"({task.label})"

            lines.append(
                f"{index:>2}. {status_col:<14} {due_col:<12} {title_col:<30} {label_col}"
            )

        return "\n".join(lines)
