from task_content_io import AbstractTaskReader, EasyTaskReader
from typing import Dict
from pprint import pprint
from abc import ABC, abstractmethod


class AbstractTranslator(ABC):
    @abstractmethod
    def translate(self, input_number, input_from_num_sys, input_to_num_sys):
        pass

    @staticmethod
    def digit_to_letter(digit):
        return chr(ord('A') + digit - 10)


class FromDecimalToAny(AbstractTranslator):
    def translate(self, input_number, input_from_num_sys, input_to_num_sys):
        print("%s(%s) = ?(%s)" % (input_number, input_from_num_sys, input_to_num_sys))
        number = int(input_number)
        from_num_sys = int(input_from_num_sys)
        to_num_sys = int(input_to_num_sys)

        mods = []
        while number > 0:
            div, mod = divmod(number, to_num_sys)
            print("{:{}d} / {:d} = {:{}d} | {:d}".format(number, 5, to_num_sys, div, 5, mod), end='')
            if mod >= 10:
                letter = self.digit_to_letter(mod)
                print(" | {:s}".format(letter))
            else:
                letter = mod
                print()
            mods.append(letter)
            number = div

        reversed_mods = mods[::-1]
        str_reversed_mods = [str(item) for item in reversed_mods]
        result_number = "".join(str_reversed_mods)

        print("{0}({1}) = {2}({3})".format(input_number, input_from_num_sys, result_number, input_to_num_sys))
        print()


def main():
    task_reader: AbstractTaskReader = EasyTaskReader()
    tasks: Dict = task_reader.get_read_tasks()

    translator: AbstractTranslator = FromDecimalToAny()
    for variant_value in tasks.values():
        actual_task: list = variant_value[1]

        translator.translate(*actual_task)
        # print(*actual_task)


if __name__ == '__main__':
    main()
