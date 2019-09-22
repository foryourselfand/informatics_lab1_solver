from task_content_io import AbstractTaskReader, EasyTaskReader
from typing import Dict
from pprint import pprint
from abc import ABC, abstractmethod


class AbstractTranslator(ABC):
    @abstractmethod
    def translate(self, input_number, from_num_sys, to_num_sys):
        pass

    @staticmethod
    def digit_to_letter(digit):
        return chr(ord('A') + digit - 10)


class FromDecimalToAny(AbstractTranslator):
    def translate(self, input_number, from_num_sys, to_num_sys):
        print("%s(%s) = ?(%s)" % (input_number, from_num_sys, to_num_sys))
        number = int(input_number)
        from_num_sys = int(from_num_sys)
        to_num_sys = int(to_num_sys)

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

        print("{0}({1}) = {2}({3})".format(input_number, from_num_sys, result_number, to_num_sys))
        print()
        return result_number


class FromAnyToDecimal(AbstractTranslator):
    def translate(self, input_number, from_num_sys, to_num_sys):
        print("%s(%s) = ?(%s)" % (input_number, from_num_sys, to_num_sys))

        number = str(input_number)
        from_num_sys = int(from_num_sys)
        to_num_sys = int(to_num_sys)

        print(input_number, end=' ')
        for run_flag in [False, True]:
            terms, expression = self.get_terms_expression_and_letter_flag(number, from_num_sys, run_flag)
            self.print_with_equality(expression)

        python_terms = [term.replace('^', '**') for term in terms]

        short_terms = []
        for term in python_terms:
            split_term = term.split(' ')
            if len(split_term) == 2:
                short_terms.append(term)
                continue
            power_str = split_term[-1]
            power_eval = eval(power_str)
            temp_term_list = split_term[:-1] + [str(power_eval)]
            term_term = " ".join(temp_term_list)
            short_terms.append(term_term)
        short_expression = " + ".join(short_terms)
        self.print_with_equality(short_expression)

        eval_terms = [eval(term) for term in short_terms]
        str_eval_terms = [str(term) for term in eval_terms]

        middle_expression = " + ".join(str_eval_terms)
        self.print_with_equality(middle_expression, end=' ')

        result_number = sum(eval_terms)
        print(result_number)

        print("{0}({1}) = {2}({3})".format(input_number, from_num_sys, result_number, to_num_sys))
        print()
        return result_number

    @staticmethod
    def print_with_equality(expression: str, end='\n'):
        print("= %s =" % expression, end=end)

    def get_terms_expression_and_letter_flag(self, number, from_num_sys, second_run=False):
        terms = []
        for digit, index in zip(number, range(len(number) - 1, -1, -1)):
            small_term = '^%d' % index
            big_term = "* %d%s" % (from_num_sys, small_term)

            if second_run:
                if digit.isalpha():
                    digit = self.letter_to_digit(digit)
                if digit == '0':
                    continue
                if index == 0:
                    big_term = ''
                if index == 1:
                    big_term = "* %d" % from_num_sys

            full_term = "%s %s" % (digit, big_term)
            terms.append(full_term)
        expression = ' + '.join(terms)
        return terms, expression

    @staticmethod
    def letter_to_digit(letter: str):
        return ord(letter) - ord('A') + 10


def main():
    task_reader: AbstractTaskReader = EasyTaskReader()
    tasks: Dict = task_reader.get_read_tasks()

    translator: AbstractTranslator = FromAnyToDecimal()
    for variant_value in tasks.values():
        actual_task: list = variant_value[2]

        translator.translate(*actual_task)
        # print(*actual_task)


if __name__ == '__main__':
    main()
