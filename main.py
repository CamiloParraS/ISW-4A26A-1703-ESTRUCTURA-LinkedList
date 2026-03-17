import tkinter as tk
from app import TodoApp

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    TodoApp(root)
    root.mainloop()
