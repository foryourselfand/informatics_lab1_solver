from task_names import BasicTaskNamesGetter
from typing import Dict, List
from pprint import pprint


class TaskGetter:
    def __init__(self, all_tasks: Dict, start: int, end: int):
        self.all_tasks: Dict = all_tasks
        self.start: int = start
        self.end: int = end
        self.task_range = end - start + 1

    def handle_line(self, line: List):
        variant = int(line[0])

        split_line = line[1:]
        for temp_task_index in range(self.task_range):
            temp_task = []
            for increment in range(3):
                index = temp_task_index * 3 + increment
                temp_task.append(split_line[index])

            if variant not in self.all_tasks.keys():
                self.all_tasks[variant] = dict()
            special_task: Dict = self.all_tasks[variant]

            real_task_index = temp_task_index + self.start
            if real_task_index not in special_task.keys():
                special_task[real_task_index] = temp_task


def get_task_names():
    task_names_creator = BasicTaskNamesGetter()
    task_names = task_names_creator.get_task_names()
    return task_names


def main():
    task_names = get_task_names()

    all_tasks: Dict = dict()

    for task_name in task_names:
        split_task_name = task_name.split('_')
        start: int = int(split_task_name[0])
        end: int = int(split_task_name[1])

        task_file_name: str = "tasks/%s.txt" % task_name
        with open(task_file_name, "r", encoding='utf-8') as file:
            task_getter = TaskGetter(all_tasks, start, end)

            lines = file.readlines()
            for line in lines:
                line = line.replace('\n', '')
                split_line = line.split(' ')

                if task_name == '10_11':
                    half_len = len(split_line) // 2

                    first_half = split_line[:half_len]
                    second_half = split_line[half_len:]

                    task_getter.handle_line(first_half)
                    task_getter.handle_line(second_half)
                else:
                    task_getter.handle_line(split_line)
    pprint(all_tasks)


if __name__ == '__main__':
    main()
