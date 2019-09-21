from abc import ABC, abstractmethod
from typing import List
from os import listdir

from config import tasks_dir_base


class AbstractTaskNamesGetter(ABC):
    def __init__(self):
        self.__task_names = []

    @abstractmethod
    def __create_task_names__(self, task_names):
        pass

    def get_task_names(self):
        self.__create_task_names__(self.__task_names)
        return self.__task_names


class BasicTaskNamesGetter(AbstractTaskNamesGetter):
    def __create_task_names__(self, task_names):
        task_names += ['1_5', '6_9', '10_11']


class DirectoryTaskNamesGetter(AbstractTaskNamesGetter):
    def __create_task_names__(self, task_names):
        full_task_names: List = listdir(tasks_dir_base)
        short_task_names: List = [task_name[:-4] for task_name in full_task_names]
        task_names += reversed(short_task_names)


class AdvanceTaskNamesGetter(AbstractTaskNamesGetter):
    def __create_task_names__(self, task_names):
        flag_numbers = self.__get_flag_numbers__()

        for i in range(len(flag_numbers)):
            start = self.__get_start__(i, flag_numbers)
            end = self.__get_end__(i, flag_numbers)

            temp_task_name = "%d_%d" % (start, end)
            task_names.append(temp_task_name)

    @abstractmethod
    def __get_flag_numbers__(self):
        pass

    @abstractmethod
    def __get_start__(self, i, flag_numbers):
        pass

    @abstractmethod
    def __get_end__(self, i, flag_numbers):
        pass


class PrefixTaskNamesGetter(AdvanceTaskNamesGetter):
    def __get_flag_numbers__(self):
        return [5, 9, 11]

    def __get_start__(self, i, flag_numbers):
        if i == 0:
            return 1
        else:
            return flag_numbers[i - 1] + 1

    def __get_end__(self, i, flag_numbers):
        return flag_numbers[i]


class PostfixTaskNamesGetter(AdvanceTaskNamesGetter):
    def __get_flag_numbers__(self):
        return [1, 6, 10]

    def __get_start__(self, i, flag_numbers):
        return flag_numbers[i]

    def __get_end__(self, i, flag_numbers):
        if i == len(flag_numbers) - 1:
            return 11
        else:
            return flag_numbers[i + 1] - 1


def main():
    for task_name_class in [BasicTaskNamesGetter, DirectoryTaskNamesGetter,
                            PrefixTaskNamesGetter, PostfixTaskNamesGetter]:
        task_names_getter: AbstractTaskNamesGetter = task_name_class()
        task_names = task_names_getter.get_task_names()
        print(*task_names)


if __name__ == '__main__':
    main()
