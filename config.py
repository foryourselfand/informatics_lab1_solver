input_tasks_dir_base = "input_tasks/"
working_tasks_dir_base = 'working_tasks/'


def get_task_name(tasks_dir_base: str = input_tasks_dir_base, file_name: str = 'tasks', file_format: str = 'txt'):
    return "%s%s.%s" % (tasks_dir_base, file_name, file_format)
