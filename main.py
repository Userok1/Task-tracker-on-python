# C:\Users\Gwyn\Desktop\python\learning\common_python\task_tracker

from enum import Enum
from datetime import datetime
import json
import os
import re
import sys
from argparse import ArgumentParser


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
        self.updatedAt = datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class TaskList:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.parser = TaskList._create_parser()
        # On the moment of initializing TaskList object we are ensuring that
        # json file exists, if not, a new one is being created
        self.__ensure_file_exists()


    @staticmethod
    def _create_parser() -> ArgumentParser:
        parser = ArgumentParser(description="The CLI task manager to work with tasks")
        subparsers = parser.add_subparsers(dest="command")

        task_cli_parser = subparsers.add_parser("task-cli")
        task_cli_subparsers = task_cli_parser.add_subparsers(dest="task_cli_command", help="task-cli manager")

        # ADD command
        add_cmd_parser = task_cli_subparsers.add_parser("add", help="Adds the task to task list")
        add_cmd_parser.add_argument("description", type=str, default="",
                                    help="Description of added task")

        # UPDATE command
        update_cmd_parser = task_cli_subparsers.add_parser("update", help="Updates the task")
        update_cmd_parser.add_argument("task_id", type=int,
                                       help="Id of updated task")
        update_cmd_parser.add_argument("description", type=str, default="",
                                       help="New description of updated task")
        
        # DELETE command
        delete_cmd_parser = task_cli_subparsers.add_parser("delete", help="Deletes task")
        delete_cmd_parser.add_argument("task_id", type=int,
                                       help="Deletes task by its id")
        
        # MARK IN-PROGRESS command
        mip_cmd_parser = task_cli_subparsers.add_parser("mark-in-progress", help="Sets task's status as 'in-progress'")
        mip_cmd_parser.add_argument("task_id", type=int,
                                    help="Task id")
        
        # MARK DONE command
        md_cmd_parser = task_cli_subparsers.add_parser("mark-done", help="Sets task's status as 'done'")
        md_cmd_parser.add_argument("task_id", type=int,
                                   help="Task id")

        # LIST TASKS command
        list_cmd_parser = task_cli_subparsers.add_parser("list", help="List all tasks")
        list_cmd_parser.add_argument("-d", "--done", action="store_true",
                                     help="Lists all tasks with 'done' status")
        list_cmd_parser.add_argument("-td", "--todo", action="store_true",
                                     help="Lists all tasks with 'todo' status")
        list_cmd_parser.add_argument("-ip", "--in-progress", action="store_true", dest="in_progress",
                                     help="Lists all tasks with 'in-progress' status")
        
        return parser
    

    def handle_commands(self, user_input: str):
        args = self.parser.parse_args(list(map(lambda s: s.strip("\""), user_input.split())))
        if args.command == "task-cli":
            tcc = args.task_cli_command

            if tcc == "add":
                self.add(args.description)
        
            elif tcc == "update":
                self.update(str(args.task_id), args.description)

            elif tcc == "delete":
                self.delete(str(args.task_id))

            elif tcc == "mark-in-progress":
                self.mark_inprogress(str(args.task_id))

            elif tcc == "mark-done":
                self.mark_done(str(args.task_id))
            
            elif tcc == "list":
                if args.done:
                    self.list_done_tasks()
                elif args.in_progress:
                    self.list_inprogress_tasks()
                elif args.todo:
                    self.list_todo_tasks()
                else:
                    self.list_tasks()


    def add(self, description: str) -> None:
        task = Task(description)
        
        data = self.__read()

        task_id = int(max(data.keys())) + 1 if len(data) > 0 else 1
        task.id = task_id
        data[task_id] = task.__dict__

        self.__save(data)

        print(f"Task added successfully (ID: {task.id})")
    

    def update(self, task_id: int, description: str) -> None:
        data = self.__read()

        if data.get(task_id, None) == None:
            print("No such task")
            return
        
        data[task_id]['description'] = description
        data[task_id]['updatedAt'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        self.__save(data)

        print(f"Task updated successfully (ID: {task_id})")


    def delete(self, task_id: int) -> None:
        data = self.__read()

        if data.get(task_id, None) == None:
            print("No such task")
            return
        
        del data[task_id]

        self.__save(data)

        print(f"Task deleted successfully (ID: {task_id})")

    
    def mark_inprogress(self, task_id: int) -> None:
        data = self.__read()

        if data.get(task_id, None) == None:
            print("No such task")
            return
        
        data[task_id]['status'] = TaskStatus.IN_PROGRESS.value
        data[task_id]['updatedAt'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        self.__save(data)

        print(f"Task marked as in-progress successfully (ID: {task_id})")

    
    def mark_done(self, task_id: int) -> None:
        data = self.__read()

        if data.get(task_id, None) == None:
            print("No such task")
            return
        
        data[task_id]['status'] = TaskStatus.DONE.value
        data[task_id]['updatedAt'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        self.__save(data)

        print(f"Task marked as done successfully (ID: {task_id})")


    def list_tasks(self) -> None:
        data = self.__read()
        
        for task_id, task in data.items():
            print(f"{task_id}: {task}")

    
    def list_done_tasks(self) -> None:
        data = self.__read()

        for task_id, task in data.items():
            if task['status'] == TaskStatus.DONE.value:
                print(f"{task_id}: {task}")

    
    def list_inprogress_tasks(self) -> None:
        data = self.__read()

        for task_id, task in data.items():
            if task['status'] == TaskStatus.IN_PROGRESS.value:
                print(f"{task_id}: {task}")


    def list_todo_tasks(self) -> None:
        data = self.__read()

        for task_id, task in data.items():
            if task['status'] == TaskStatus.TODO.value:
                print(f"{task_id}: {task}")


    def __read(self) -> dict:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
       
        return data
    

    def __save(self, data: dict) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    

    def __ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open("tasks.json", 'w') as f:
                json.dump({}, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    tl = TaskList("./tasks.json")

    try:
        while True:
            user_input = input(">> ")

            if not user_input:
                continue

            try:
                tl.handle_commands(user_input.strip())
            except SystemExit:
                continue
    except KeyboardInterrupt:
        print("\nEnd of program")