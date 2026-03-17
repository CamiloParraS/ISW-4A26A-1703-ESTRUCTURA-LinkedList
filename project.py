from __future__ import annotations
from todo_node import TodoNode


class Project:
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
