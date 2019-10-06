from task_content_io import AbstractTaskReader, EasyTaskReader
from typing import Dict
from pprint import pprint
from abc import ABC, abstractmethod
from sys import argv
from math import log


class AbstractTranslator(ABC):
    def translate(self, input_number, from_num_sys, to_num_sys):
        self.__print_template(input_number, from_num_sys, '?', to_num_sys)

        result_number = self.__actual_translate__(input_number, from_num_sys, to_num_sys)

        self.__print_template(input_number, from_num_sys, result_number, to_num_sys)

        return result_number

    @staticmethod
    def __print_template(input_number, from_num_sys, result_number, to_num_sys):
        print(f'{input_number}({from_num_sys}) = {result_number}({to_num_sys})')

    @abstractmethod
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):
        pass

    @staticmethod
    def digit_to_letter(digit):
        if 0 <= digit <= 9:
            return str(digit)
        else:
            return chr(ord('A') + digit - 10)

    @staticmethod
    def letter_to_digit(letter: str):
        return ord(letter) - ord('A') + 10


class FromDecimalToAny(AbstractTranslator):
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):
        number = str(input_number)
        from_num_sys = int(from_num_sys)
        to_num_sys = int(to_num_sys)

        number_split = number.split(',')

        if len(number_split) == 1:
            translator = FromDecimalToAnyWhole()
            result_number = translator.__actual_translate__(input_number, from_num_sys, to_num_sys)
        else:
            whole_input = number_split[0]
            fractional_input = float(f'0.{number_split[1]}')

            whole_translator = FromDecimalToAnyWhole()
            fractional_translator = FromDecimalToAnyFractional()

            whole_result = whole_translator.translate(whole_input, from_num_sys, to_num_sys)
            fractional_result = fractional_translator.translate(fractional_input, from_num_sys, to_num_sys)

            result_number = whole_result + fractional_result[1:]
            format_str = '{}({from_ns}) = {}({from_ns}) + {}({from_ns}) = {}({to_ns}) + {}({to_ns}) = {}({to_ns})'
            print(format_str.format(input_number,
                                    whole_input, fractional_input,
                                    whole_result, fractional_result,
                                    result_number,
                                    from_ns=from_num_sys,
                                    to_ns=to_num_sys))

        return result_number


class FromDecimalToAnyWhole(AbstractTranslator):
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):
        number = int(input_number)

        mods = []
        while number > 0:
            div, mod = divmod(number, to_num_sys)
            print('{:{}d} / {:d} = {:{}d} | {:d}'.format(number, 6, to_num_sys, div, 6, mod), end='')
            if mod >= 10:
                letter = self.digit_to_letter(mod)
                print(' | {:s}'.format(letter))
            else:
                letter = mod
                print()
            mods.append(letter)
            number = div

        reversed_mods = mods[::-1]
        str_reversed_mods = [str(item) for item in reversed_mods]
        str_result = ''.join(str_reversed_mods)

        return str_result


class FromDecimalToAnyFractional(AbstractTranslator):
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):
        # number = float(f'0.{input_number}')
        number = input_number

        whole_and_reminder = str(input_number).split('.')
        self.beauty_print(whole_and_reminder[0], whole_and_reminder[1], to_num_sys, True)
        wholes = []
        for i in range(5):
            number *= to_num_sys

            number_split = str(number).split('.')
            temp_whole = number_split[0]
            remainder = number_split[1]
            self.beauty_print(temp_whole, remainder, to_num_sys)
            wholes.append(temp_whole)
            if remainder == '0':
                break
            number = float(f'0.{remainder}')

        str_result = ''.join(wholes)
        float_result = float(f'0.{str_result}')
        format_result = '{:.5f}'.format(float_result)

        return format_result

    @staticmethod
    def beauty_print(temp_whole, remainder, to_num_sys, hide=False):
        if hide:
            temp_whole = f'({temp_whole})'
        whole_part = '{:^{}s}|'.format(temp_whole, 3)
        whole_and_reminder = '{} {:{}s}'.format(whole_part, remainder, 2)
        print(whole_and_reminder)
        print('{:>{}} {}'.format('|', len(whole_part), to_num_sys))
        print('—' * len(whole_and_reminder))


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
            term_term = ' '.join(temp_term_list)
            short_terms.append(term_term)
        short_expression = ' + '.join(short_terms)
        self.print_with_equality(short_expression)

        eval_terms = [eval(term) for term in short_terms]
        str_eval_terms = [str(term) for term in eval_terms]

        middle_expression = ' + '.join(str_eval_terms)
        self.print_with_equality(middle_expression, end=' ')

        result_number = sum(eval_terms)
        print(result_number)

        return result_number

    @staticmethod
    def print_with_equality(expression: str, end='\n'):
        print('= %s =' % expression, end=end)

    def get_terms_expression_and_letter_flag(self, number, from_num_sys, second_run=False):
        terms = []
        for digit, index in zip(number, range(len(number) - 1, -1, -1)):
            small_term = '^%d' % index
            big_term = '* %d%s' % (from_num_sys, small_term)

            if second_run:
                if digit.isalpha():
                    digit = self.letter_to_digit(digit)
                if digit == '0':
                    continue
                if index == 0:
                    big_term = ''
                if index == 1:
                    big_term = '* %d' % from_num_sys

            full_term = '%s %s' % (digit, big_term)
            terms.append(full_term)
        expression = ' + '.join(terms)
        return terms, expression


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


class ShortTranslator(AbstractTranslator, ABC):
    def __init__(self):
        self.base_to_res_tables: Dict[int, Dict[str, str]] = self.get_base_to_res_table()
        self.res_to_base_tables: Dict[int, Dict[str, str]] = self.get_res_to_base_table(self.base_to_res_tables)

        pprint(self.base_to_res_tables)
        # pprint(self.res_to_base_tables)

    def get_base_table(self, base: int = 2, power: int = 4):
        table: Dict[str: str] = dict()
        for i in range(base ** power):
            row = []
            for j in range(power - 1, -1, -1):
                temp = ((i // (base ** j)) % base)
                row.append(str(temp))

            key = ''.join(row)
            value = self.digit_to_letter(i)

            table[key] = value
        return table

    @staticmethod
    def get_shorted_table(base_table: Dict[str, str], base: int = 2, power: int = 4):
        new_table: Dict[str, str] = dict()
        for index, item in enumerate(base_table.items()):
            if index == base ** power:
                break
            old_key = item[0]
            value = item[1]

            new_key = old_key[len(old_key) - power:]
            new_table[new_key] = value
        return new_table

    def get_base_to_res_table(self, base: int = 2, power: int = 4):
        table: Dict[int, Dict[str, str]] = dict()
        table[base ** power] = self.get_base_table()
        for i in range(power - 1, 1, -1):
            table[base ** i] = self.get_shorted_table(table[base ** power], base=base, power=i)
        return table

    def get_res_to_base_table(self, base_table):
        table: Dict[int, Dict[str, str]] = dict()
        for key, base_to_res in base_table.items():
            table[key] = dict()
            for base, rez in base_to_res.items():
                table[key][rez] = base
        return table

    def get_and_print_power(self, first: int, second: int):
        max_n = max(first, second)
        min_n = min(first, second)
        power = int(log(max_n, min_n))
        print(f"{max_n} = {min_n}^{power}")

        return power

    def remove_leading_zeroes(self, number: str, from_end: bool = False):
        if from_end:
            number = number[::-1]

        zero_flag = True
        result_number = []
        for char in number:
            if char != '0' and zero_flag:
                zero_flag = False
            if not zero_flag:
                result_number.append(char)

        if from_end:
            result_number = result_number[::-1]

        result = ''.join(result_number)
        return result

    def add_leading_zeros(self, number: str, power: int, from_end: bool = False):
        missing_count = power - (len(number) % power)
        missing_zeroes = '0' * missing_count
        if from_end:
            return number + missing_zeroes
        else:
            return missing_zeroes + number


class FromBigToSmallShort(ShortTranslator):
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):
        number = str(input_number)
        from_num_sys = int(from_num_sys)
        to_num_sys = int(to_num_sys)

        power = self.get_and_print_power(to_num_sys, from_num_sys)

        in_whole, in_remainder = number.split(',')

        out_whole = self.detailed_print(in_whole, from_num_sys, to_num_sys, False)
        out_remainder = self.detailed_print(in_remainder, from_num_sys, to_num_sys, True)
        result = "{},{:.5}".format(out_whole, out_remainder)

        return result

    def detailed_print(self, number, from_num_sys, to_num_sys, from_end):
        in_full = f'{number}({from_num_sys})'
        in_with_spaces = ' '.join(number)

        outs = []
        for elem in number:
            outs.append(self.res_to_base_tables[from_num_sys][elem])

        out_with_spaces = ' '.join(outs)
        out_without_spaces = ''.join(outs)

        out_without_leading_zeroes = self.remove_leading_zeroes(out_without_spaces, from_end)
        out_full = f'{out_without_leading_zeroes}({to_num_sys})'

        print(' = '.join([in_full, in_with_spaces, out_with_spaces, out_full]))

        return out_without_leading_zeroes


class FromSmallToBigShort(ShortTranslator):
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):
        number = str(input_number)
        from_num_sys = int(from_num_sys)
        to_num_sys = int(to_num_sys)

        power = self.get_and_print_power(from_num_sys, to_num_sys)

        in_whole, in_remainder = number.split(',')
        out_whole = self.detailed_print(in_whole, from_num_sys, to_num_sys, power, False)
        out_remainder = self.detailed_print(in_remainder, from_num_sys, to_num_sys, power, True)
        result = "{},{:.5}".format(out_whole, out_remainder)

        return result

    def detailed_print(self, number, from_num_sys, to_num_sys, power: int, from_end):
        in_full = f'{number}({from_num_sys})'
        in_with_leading_zeroes = self.add_leading_zeros(number, power, from_end)

        wanted_parts = len(in_with_leading_zeroes) // power
        ins_with_spaces = self.split_list(in_with_leading_zeroes, wanted_parts)
        in_with_spaces = ' '.join(ins_with_spaces)

        outs = []
        for elem in ins_with_spaces:
            outs.append(self.base_to_res_tables[to_num_sys][elem])

        out_with_spaces = ' '.join(outs)
        out_without_spaces = ''.join(outs)

        out_full = f'{out_without_spaces}({to_num_sys})'

        print(' = '.join([in_full, in_with_spaces, out_with_spaces, out_full]))

        return out_without_spaces

    @staticmethod
    def split_list(wanted_list, wanted_parts=1):
        length = len(wanted_list)
        return [wanted_list[i * length // wanted_parts: (i + 1) * length // wanted_parts]
                for i in range(wanted_parts)]


def main():
    task_number = int(argv[1]) if len(argv) == 2 else 1

    task_reader: AbstractTaskReader = EasyTaskReader()
    tasks: Dict = task_reader.get_read_tasks()

    translators = {1: FromDecimalToAny(),
                   2: FromAnyToDecimal(),
                   3: FromAnyToAny(),
                   4: FromDecimalToAny(),
                   5: FromBigToSmallShort(),
                   6: FromBigToSmallShort(),
                   7: FromSmallToBigShort()}

    translator: AbstractTranslator = translators[task_number]
    for variant_value in tasks.values():
        actual_task: list = variant_value[task_number]

        translator.translate(*actual_task)
        print()


if __name__ == '__main__':
    main()
