# Task-tracker-on-python
First project on python

The project is a simple task tracker cli interface thas allows users to manage tasks (add, update, delete)
and mark them with different status (like to-do, in-progress, done)

You have list of commands:
* task-cli add ['description'] (this command adds a new task to the task list with the 'description')
* task-cli update [id] ['description'] (this command selects task from task list by its id and updates it 'description')
* task-cli delete [id] (this command deletes a task by its id from the list)
* task-cli mark-in-progress [id] (this command sets a task's status as _in-progress_)
* task-cli mark-done [id] (this command sets a task's status as _done_)
* task-cli list
* task-cli list done
* task-cli list in-progress
* task-cli list todo

Tasks have ids so you can choose the specific one and invoke a command you want to.
You have the possability list tasks (all of them and by the status).
Thats all.
Thank you.


Project is for https://roadmap.sh/projects/task-tracker
