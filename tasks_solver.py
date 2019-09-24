from task_content_io import AbstractTaskReader, EasyTaskReader
from typing import Dict
from pprint import pprint
from abc import ABC, abstractmethod
from sys import argv


class AbstractTranslator(ABC):
    def translate(self, input_number, from_num_sys, to_num_sys):
        self.__print_template(input_number, from_num_sys, "?", to_num_sys)

        result_number = self.__actual_translate__(input_number, from_num_sys, to_num_sys)

        self.__print_template(input_number, from_num_sys, result_number, to_num_sys)
        print()

        return result_number

    @staticmethod
    def __print_template(input_number, from_num_sys, result_number, to_num_sys):
        print(f"{input_number}({from_num_sys}) = {result_number}({to_num_sys})")

    @abstractmethod
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):
        pass

    @staticmethod
    def digit_to_letter(digit):
        return chr(ord('A') + digit - 10)


class FromDecimalToAny(AbstractTranslator):
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):
        number = str(input_number)
        from_num_sys = int(from_num_sys)
        to_num_sys = int(to_num_sys)

        number_split = number.split(',')
        whole_part = int(number_split[0])

        whole_part_result = self.translate_whole_part(whole_part, from_num_sys, to_num_sys)
        result_number = whole_part_result

        if len(number_split) == 2:
            fractional_part = int(number_split[1])
            fractional_part_result = self.translate_fractional_part(fractional_part, from_num_sys, to_num_sys)

            result_number += fractional_part_result

        return result_number

    def translate_whole_part(self, whole_part, from_num_sys, to_num_sys):
        number = whole_part

        mods = []
        while number > 0:
            div, mod = divmod(number, to_num_sys)
            print("{:{}d} / {:d} = {:{}d} | {:d}".format(number, 6, to_num_sys, div, 6, mod), end='')
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
        result = "".join(str_reversed_mods)

        return result

    def translate_fractional_part(self, fractional_part, from_num_sys, to_num_sys):
        number = float(f'0.{fractional_part}')

        wholes = []
        for i in range(5):
            number *= to_num_sys

            number_split = str(number).split('.')

            temp_whole = number_split[0]
            wholes.append(temp_whole)

            remainder = number_split[1]
            print("{:{}s} | {:{}s}".format(temp_whole, 5, remainder, 5))
            if remainder == '0':
                break
            number = float(f'0.{remainder}')

        str_result = "".join(wholes)
        result = f'0.{str_result}'
        print(result)

        return result


class FromAnyToDecimal(AbstractTranslator):
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):

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


class FromAnyToAny(AbstractTranslator):
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):
        number = str(input_number)
        from_num_sys = int(from_num_sys)
        to_num_sys = int(to_num_sys)

        from_any_to_decimal = FromAnyToDecimal()
        decimal_number = from_any_to_decimal.translate(number, from_num_sys, 10)

        from_decimal_to_any = FromDecimalToAny()
        result_number = from_decimal_to_any.translate(decimal_number, 10, to_num_sys)

        return result_number


def main():
    task_number = int(argv[1]) if len(argv) == 2 else 1

    task_reader: AbstractTaskReader = EasyTaskReader()
    tasks: Dict = task_reader.get_read_tasks()

    translators = {1: FromDecimalToAny(),
                   2: FromAnyToDecimal(),
                   3: FromAnyToAny(),
                   4: FromDecimalToAny()}

    translator: AbstractTranslator = translators[task_number]
    # translator.translate('1,8125', 10, 2)
    for variant_value in tasks.values():
        actual_task: list = variant_value[task_number]

        translator.translate(*actual_task)
        # print(*actual_task)


if __name__ == '__main__':
    main()
