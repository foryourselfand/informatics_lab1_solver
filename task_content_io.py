from abc import ABC, abstractmethod
from task_name_creator import DirectoryTaskNamesGetter, BasicTaskNamesGetter, AbstractTaskNamesGetter
from typing import Dict, List, Tuple
from pprint import pprint
from config import get_task_name, working_tasks_dir_base
from collections import defaultdict
import pickle


class AbstractTaskReader(ABC):
    @abstractmethod
    def get_read_tasks(self) -> Dict[int, Dict[int, List[str]]]:
        pass


class AbstractTaskWriter(ABC):
    def __init__(self):
        short_file_name, file_format = self.__get_file_name_and_format__()
        self.__full_file_name__ = get_task_name(working_tasks_dir_base, short_file_name, file_format)

    @abstractmethod
    def __get_file_name_and_format__(self) -> Tuple[str, str]:
        pass

    @abstractmethod
    def write_tasks(self, tasks: Dict):
        pass


class HardTaskReader(AbstractTaskReader):
    def __init__(self, task_name_creator: AbstractTaskNamesGetter):
        self.task_names = task_name_creator.get_task_names()
        self.task_split_parts = {'10_11': 2}

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

            task_file_name = get_task_name(file_name=task_name)
            with open(task_file_name, 'r', encoding='utf-8') as file:
                for line in file.readlines():
                    line = line.replace('\n', '')
                    line_list = line.split(' ')

                    split_lines = self.split_list(line_list, split_parts)
                    for split_line in split_lines:
                        task_getter.handle_line(split_line)
        return dict(tasks)


class EasyTaskReader(AbstractTaskReader):
    def get_read_tasks(self) -> Dict[int, Dict[int, List[str]]]:
        file_name = get_task_name(working_tasks_dir_base, 'pickle_tasks', 'pickle')
        with open(file_name, 'rb') as file:
            tasks = pickle.load(file)
        return tasks


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
            real_task_index = temp_task_index + self.start
            temp_task = [split_line[temp_task_index * 3 + increment] for increment in range(3)]
            special_task[real_task_index] = temp_task


class DumpTaskWriter(AbstractTaskWriter):
    def __get_file_name_and_format__(self) -> Tuple[str, str]:
        return 'pickle_tasks', 'pickle'

    def write_tasks(self, tasks: Dict):
        with open(self.__full_file_name__, 'wb') as file:
            pickle.dump(tasks, file)


def main():
    names_creator: AbstractTaskNamesGetter = DirectoryTaskNamesGetter()
    task_reader: AbstractTaskReader = HardTaskReader(names_creator)

    tasks: Dict = task_reader.get_read_tasks()
    pprint(tasks)

    task_writer: AbstractTaskWriter = DumpTaskWriter()
    task_writer.write_tasks(tasks)


if __name__ == '__main__':
    main()
