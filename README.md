# Task-tracker-on-python
First project on python

The project is a simple task tracker cli interface thas allows users to manage tasks (add, update, delete)
and mark them with different status (like to-do, in-progress, done)

You have list of commands:
* task-cli add ['description'] (this command adds a new task to the task list with the 'description')
* task-cli update [id] ['description'] (this command selects task from task list by its id and updates it 'description')
* task-cli delete [id] (this command deletes a task by its id from the list)
* task-cli mark-in-progress [id] (this command sets a task's status as ***in-progress***)
* task-cli mark-done [id] (this command sets a task's status as ***done***)
* task-cli list (this command writes out the list of tasks)
* task-cli list done (similar as 'task-cli list' this command writes out the list but only tasks with ***done*** status)
* task-cli list in-progress (similar as 'task-cli list' this command writes out the list but only tasks with ***in-progress*** status)
* task-cli list todo (similar as 'task-cli list' this command writes out the list but only tasks with ***todo*** status)

Tasks have ids so you can choose the specific one and invoke a command on you want to.
You have the possability list tasks (all of them and by the status)


Project is for [https://roadmap.sh/projects/task-tracker](https://roadmap.sh/projects/task-tracker)
