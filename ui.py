import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import os
from datetime import datetime, timedelta

TODO_FILE = 'todo.csv'
DONE_FILE = 'done.csv'

class MyToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MyToDo")
        self.root.geometry("1000x650")

        self.sort_column = None
        self.sort_reverse = False

        self.create_widgets()
        self.load_data()
        self.update_row_colors()
        self.root.after(60000, self.schedule_row_color_update)  # 1分ごとに更新

    def create_widgets(self):
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10)

        labels = ["登録日", "工事コード", "案件名", "内容", "予定工数", "締切日"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(frame_input, text=label).grid(row=0, column=i)
            entry = tk.Entry(frame_input, width=15)
            entry.grid(row=1, column=i, padx=2)
            self.entries[label] = entry

        self.entries["登録日"].insert(0, datetime.today().strftime("%Y-%m-%d"))

        btn_register = tk.Button(self.root, text="登録!", command=self.register_task)
        btn_register.pack(pady=5)

        columns = tuple(labels)
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', height=15)
        self.tree.pack(pady=10, fill='x')

        for col in columns:
            width = 150 if col in ["案件名", "内容"] else 100
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_by_column(_col))
            self.tree.column(col, width=width, anchor='w')

        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=("Helvetica", 11))
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

        self.tree.bind("<Double-1>", self.on_tree_item_double_click)

        btn_done_view = tk.Button(self.root, text="完了タスク画面", command=self.open_done_window)
        btn_done_view.pack(pady=5)

    def register_task(self):
        values = [self.entries[label].get() for label in self.entries]
        if not any(values):
            messagebox.showwarning("警告", "少なくとも1つの項目を入力してください。")
            return
        self.tree.insert('', 'end', values=values)
        self.save_data()
        self.update_row_colors()
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries["登録日"].insert(0, datetime.today().strftime("%Y-%m-%d"))

    def on_tree_item_double_click(self, event):
        item = self.tree.selection()[0]
        popup = tk.Toplevel(self.root)
        popup.title("編集または完了")
        popup.geometry("250x100+300+200")

        tk.Button(popup, text="編集", command=lambda: self.edit_task(item, popup)).pack(padx=20, pady=10)
        tk.Button(popup, text="完了", command=lambda: self.complete_task(item, popup)).pack(padx=20, pady=10)

    def edit_task(self, item, popup):
        popup.destroy()
        values = self.tree.item(item, 'values')
        edit_win = tk.Toplevel(self.root)
        edit_win.title("タスク編集")

        entries = []
        for i, label in enumerate(["登録日", "工事コード", "案件名", "内容", "予定工数", "締切日"]):
            tk.Label(edit_win, text=label).grid(row=0, column=i)
            entry = tk.Entry(edit_win, width=15)
            entry.insert(0, values[i])
            entry.grid(row=1, column=i)
            entries.append(entry)

        def save_edit():
            new_values = [e.get() for e in entries]
            self.tree.item(item, values=new_values)
            self.save_data()
            self.update_row_colors()
            edit_win.destroy()

        tk.Button(edit_win, text="保存", command=save_edit).grid(row=2, columnspan=6, pady=10)

    def complete_task(self, item, popup):
        popup.destroy()
        values = self.tree.item(item, 'values')
        self.save_done_data(values)
        self.tree.delete(item)
        self.save_data()

    def save_data(self):
        with open(TODO_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for item in self.tree.get_children():
                writer.writerow(self.tree.item(item)['values'])

    def save_done_data(self, data):
        with open(DONE_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def load_data(self):
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.tree.insert('', 'end', values=row)

    def open_done_window(self):
        done_win = tk.Toplevel(self.root)
        done_win.title("完了タスク一覧")
        done_win.geometry("900x400")

        columns = ("登録日", "工事コード", "案件名", "内容", "予定工数", "締切日")
        tree_done = ttk.Treeview(done_win, columns=columns, show='headings', height=15)
        tree_done.pack(pady=10, fill='x')

        for col in columns:
            width = 150 if col in ["案件名", "内容"] else 100
            tree_done.heading(col, text=col)
            tree_done.column(col, width=width, anchor='w')

        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=("Helvetica", 11))

        if os.path.exists(DONE_FILE):
            with open(DONE_FILE, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    tree_done.insert('', 'end', values=row)

    def update_row_colors(self):
        today = datetime.today()
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            try:
                deadline = datetime.strptime(values[5], "%Y-%m-%d")
                if deadline < today:
                    self.tree.item(item, tags=('past',))
                elif deadline.date() == (today + timedelta(days=1)).date():
                    self.tree.item(item, tags=('warning',))
                else:
                    self.tree.item(item, tags=())
            except:
                self.tree.item(item, tags=())

        self.tree.tag_configure('warning', background='yellow')
        self.tree.tag_configure('past', background='lightcoral')

    def schedule_row_color_update(self):
        self.update_row_colors()
        self.root.after(60000, self.schedule_row_color_update)  # 毎分更新

    def sort_by_column(self, col):
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            data.sort(key=lambda t: datetime.strptime(t[0], "%Y-%m-%d"), reverse=self.sort_reverse)
        except:
            data.sort(reverse=self.sort_reverse)

        for index, (val, k) in enumerate(data):
            self.tree.move(k, '', index)

        self.sort_reverse = not self.sort_reverse
        self.sort_column = col

if __name__ == "__main__":
    root = tk.Tk()
    app = MyToDoApp(root)
    root.mainloop()
