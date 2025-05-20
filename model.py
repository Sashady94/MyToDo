import csv
import os

class TaskModel:
    def __init__(self):
        self.tasks = []
        self.done_tasks = []
        self.todo_path = "data/todo.csv"
        self.done_path = "data/done.csv"
        os.makedirs("data", exist_ok=True)

    def load_data(self):
        self.tasks = self._load_csv(self.todo_path)
        self.done_tasks = self._load_csv(self.done_path)

    def save_data(self):
        self._save_csv(self.todo_path, self.tasks)
        self._save_csv(self.done_path, self.done_tasks)

    def _load_csv(self, path):
        if not os.path.exists(path):
            return []
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            return list(reader)

    def _save_csv(self, path, data):
        with open(path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
