from model import TaskModel

class Controller:
    def __init__(self):
        self.model = TaskModel()
        self.model.load_data()

    def add_task(self, task_data):
        self.model.tasks.append([
            task_data.get("登録日", ""),
            task_data.get("工事コード", ""),
            task_data.get("案件名", ""),
            task_data.get("内容", ""),
            task_data.get("予定工数", ""),
            task_data.get("締切日", "")
        ])
        self.model.save_data()

    def get_tasks(self):
        return self.model.tasks

    def update_task(self, index, new_data):
        self.model.tasks[index] = [
            new_data.get("登録日", ""),
            new_data.get("工事コード", ""),
            new_data.get("案件名", ""),
            new_data.get("内容", ""),
            new_data.get("予定工数", ""),
            new_data.get("締切日", "")
        ]
        self.model.save_data()

    def complete_task(self, index):
        task = self.model.tasks.pop(index)
        self.model.done_tasks.append(task)
        self.model.save_data()

    def get_done_tasks(self):
        return self.model.done_tasks
