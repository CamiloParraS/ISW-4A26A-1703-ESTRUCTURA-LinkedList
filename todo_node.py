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
