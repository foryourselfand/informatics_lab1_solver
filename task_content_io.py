from abc import ABC, abstractmethod
from task_name_creator import DirectoryTaskNamesGetter, BasicTaskNamesGetter, AbstractTaskNamesGetter
from typing import Dict, List
from pprint import pprint
from config import get_task_name
from collections import defaultdict


class AbstractTaskReader(ABC):
    @abstractmethod
    def get_read_tasks(self) -> Dict[int, Dict[int, List[str]]]:
        pass


class HardTaskReader(AbstractTaskReader):
    def __init__(self, task_name_creator: AbstractTaskNamesGetter):
        self.task_names = task_name_creator.get_task_names()
        self.task_split_parts = {"10_11": 2}

    @staticmethod
    def split_list(wanted_list, wanted_parts=1):
        length = len(wanted_list)
        return [wanted_list[i * length // wanted_parts: (i + 1) * length // wanted_parts]
                for i in range(wanted_parts)]

    def get_read_tasks(self) -> Dict[int, Dict[int, List[str]]]:
        tasks: defaultdict[int, Dict[int, List[str]]] = defaultdict(dict)

        for task_name in self.task_names:
            split_parts = self.task_split_parts.get(task_name, 1)

            split_task_name = task_name.split('_')
            start: int = int(split_task_name[0])
            end: int = int(split_task_name[1])
            task_getter = TaskGetter(tasks, start, end)

            task_file_name = get_task_name(task_name)
            with open(task_file_name, 'r', encoding='utf-8') as file:
                for line in file.readlines():
                    line = line.replace('\n', '')
                    line_list = line.split(' ')

                    split_lines = self.split_list(line_list, split_parts)
                    for split_line in split_lines:
                        task_getter.handle_line(split_line)
        return dict(tasks)


class TaskGetter:
    def __init__(self, all_tasks, start: int, end: int):
        self.all_tasks = all_tasks
        self.start: int = start
        self.task_range: int = end - start + 1

    def handle_line(self, line: List):
        variant = int(line[0])
        special_task: Dict = self.all_tasks[variant]

        split_line = line[1:]
        for temp_task_index in range(self.task_range):
            temp_task = []
            for increment in range(3):
                index = temp_task_index * 3 + increment
                temp_task.append(split_line[index])

            real_task_index = temp_task_index + self.start
            special_task[real_task_index] = temp_task


def main():
    names_creator = DirectoryTaskNamesGetter()
    hard_task_reader = HardTaskReader(names_creator)

    tasks: Dict = hard_task_reader.get_read_tasks()
    pprint(tasks)


if __name__ == '__main__':
    main()
