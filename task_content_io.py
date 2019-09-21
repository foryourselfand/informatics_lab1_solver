from abc import ABC, abstractmethod
from task_name_creator import DirectoryTaskNamesGetter, BasicTaskNamesGetter, AbstractTaskNamesGetter
from typing import Dict, List
from pprint import pprint
from config import get_task_name


class TaskGetter:
    def __init__(self, all_tasks: Dict, start: int, end: int):
        self.all_tasks: Dict = all_tasks
        self.start: int = start
        self.end: int = end
        self.task_range: int = end - start + 1

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


class AbstractTaskReader(ABC):
    def __init__(self):
        self.__tasks__: Dict[int, Dict[int, List[str]]] = dict()

    def get_tasks(self) -> Dict[int, Dict[int, List[str]]]:
        self.__read_task_content__()
        return self.__tasks__

    @abstractmethod
    def __read_task_content__(self):
        pass


class HardTaskReader(AbstractTaskReader):
    def __init__(self, task_name_creator: AbstractTaskNamesGetter):
        super().__init__()
        self.task_names = task_name_creator.get_task_names()

    def __read_task_content__(self):
        for task_name in self.task_names:
            split_task_name = task_name.split('_')
            start: int = int(split_task_name[0])
            end: int = int(split_task_name[1])

            task_file_name: str = get_task_name(task_name)
            with open(task_file_name, "r", encoding='utf-8') as file:
                task_getter = TaskGetter(self.__tasks__, start, end)

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


def main():
    names_creator: AbstractTaskNamesGetter = DirectoryTaskNamesGetter()
    hard_task_reader = HardTaskReader(names_creator)

    tasks: Dict = hard_task_reader.get_tasks()

    pprint(tasks)


if __name__ == '__main__':
    main()
