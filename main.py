from enum import Enum
from datetime import datetime
import json
import os
import re


class TaskStatus(Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in-progress'
    DONE = 'done'


class Task:

    def __init__(self, description: str):
        self.id = None
        self.description = description
        self.status = TaskStatus.TODO.value
        self.createdAt = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.updatedAt = None


class TaskList:
    
    def __init__(self, file_path):
        self.file_path = file_path
        # On the moment of initializing TaskList object we are ensuring that
        # json file exists, if not, a new one is being created
        self._ensure_file_exists()


    def add(self, description: str) -> None:
        task = Task(description)
        
        data = self.read()

        task_id = int(max(data.keys())) + 1 if len(data) > 0 else 1
        task.id = task_id
        data[task_id] = task.__dict__

        self.save(data)

        print(f"Task added successfully (ID: {task.id})")
    

    def update(self, task_id: int, description: str) -> None:
        data = self.read()

        if data.get(task_id, None) == None:
            print("No such task")
            return
        
        data[task_id]['description'] = description
        data[task_id]['updatedAt'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        self.save(data)

        print(f"Task updated successfully (ID: {task_id})")


    def delete(self, task_id: int) -> None:
        data = self.read()

        if data.get(task_id, None) == None:
            print("No such task")
            return
        
        del data[task_id]

        self.save(data)

        print(f"Task deleted successfully (ID: {task_id})")

    
    def mark_inprogress(self, task_id: int) -> None:
        data = self.read()

        if data.get(task_id, None) == None:
            print("No such task")
            return
        
        data[task_id]['status'] = TaskStatus.IN_PROGRESS.value
        data[task_id]['updatedAt'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        self.save(data)

        print(f"Task marked as in-progress successfully (ID: {task_id})")

    
    def mark_done(self, task_id: int) -> None:
        data = self.read()

        if data.get(task_id, None) == None:
            print("No such task")
            return
        
        data[task_id]['status'] = TaskStatus.DONE.value
        data[task_id]['updatedAt'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        self.save(data)

        print(f"Task marked as done successfully (ID: {task_id})")


    def list_tasks(self) -> None:
        data = self.read()
        
        for task_id, task in data.items():
            print(f"{task_id}: {task}")

    
    def list_done_tasks(self) -> None:
        data = self.read()

        for task_id, task in data.items():
            if task['status'] == TaskStatus.DONE.value:
                print(f"{task_id}: {task}")

    
    def list_inprogress_tasks(self) -> None:
        data = self.read()

        for task_id, task in data.items():
            if task['status'] == TaskStatus.IN_PROGRESS.value:
                print(f"{task_id}: {task}")


    def list_todo_tasks(self) -> None:
        data = self.read()

        for task_id, task in data.items():
            if task['status'] == TaskStatus.TODO.value:
                print(f"{task_id}: {task}")


    def read(self) -> dict:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
       
        return data
    

    def save(self, data: dict) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open("tasks.json", 'w') as f:
                json.dump({}, f, indent=2, ensure_ascii=False)
    

if __name__ == '__main__':
    help_text = "Commands:\n" \
    "task-cli add ['description'] (description is description)\n" \
    "task-cli update [id] ['description'] (id is a task id)\n" \
    "task-cli delete [id] (id is a task id)\n" \
    "task-cli mark-in-progress [id] (id is a task id)\n" \
    "task-cli mark-done [id] (id is a task id)\n" \
    "task-cli list\n" \
    "task-cli list done\n" \
    "task-cli list in-progress\n" \
    "task-cli list todo\n"
    print(help_text)

    tl = TaskList("./tasks.json")

    try:
        while True:
            cmd = input("Choose one of the listed commands: ")
            # Using mostly regular expression for user inputs
            if re.match(r"task-cli add '\b[A-Za-z\d\s]+\b'", cmd):
                tl.add(cmd.split("'")[-2])
            elif re.match(r"task-cli update \d+ '\b[A-Za-z\d\s]+\b'", cmd):
                tl.update(cmd.split()[2], cmd.split("'")[-2])
            elif re.match(r"task-cli delete \d+", cmd):
                tl.delete(cmd.split()[-1])
            elif re.match(r"task-cli mark-in-progress \d+", cmd):
                tl.mark_inprogress(cmd.split()[-1])
            elif re.match(r"task-cli mark-done \d+", cmd):
                tl.mark_done(cmd.split()[-1])

            elif cmd == "task-cli list":
                tl.list_tasks()
            elif cmd == "task-cli list done":
                tl.list_done_tasks()
            elif cmd == "task-cli list in-progress":
                tl.list_inprogress_tasks()
            elif cmd == "task-cli list todo":
                tl.list_todo_tasks()
            else:
                print("No such command")
    except KeyboardInterrupt:
        print("\nEnd of program")