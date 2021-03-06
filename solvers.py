from task_content_io import AbstractTaskReader, EasyTaskReader
from typing import Dict, List
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
        if len(mods) == 0:
            mods = [0]

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
            temp_whole_letter = AbstractTranslator.digit_to_letter(int(temp_whole))
            remainder = number_split[1]
            self.beauty_print(temp_whole, remainder, to_num_sys)
            wholes.append(temp_whole_letter)
            if remainder == '0':
                break
            number = float(f'0.{remainder}')

        str_result = ''.join(wholes)
        float_result = f'0.{str_result}'
        # format_result = '{:.5f}'.format(float_result)

        return float_result
        # return format_result

    @staticmethod
    def beauty_print(temp_whole, remainder, to_num_sys, hide=False):
        temp_whole_letter = AbstractTranslator.digit_to_letter(int(temp_whole))
        if hide or temp_whole != temp_whole_letter:
            temp_whole = f'({temp_whole})'
        whole_part = '{:^{}s}|'.format(temp_whole, 4)
        whole_and_reminder = '{} {:{}s}'.format(whole_part, remainder, 3)

        whole_part_letter = '{:>{}}'.format('|', len(whole_part))
        if temp_whole != temp_whole_letter:
            whole_part_letter = '{:^{}s}|'.format(temp_whole_letter, 4)
        whole_and_reminder_letter = '{} {}'.format(whole_part_letter, to_num_sys)

        print(whole_and_reminder)
        print(whole_and_reminder_letter)
        print('—' * len(whole_and_reminder))


class FromAnyToDecimal(AbstractTranslator):
    def __actual_translate__(self, input_number, from_num_sys, to_num_sys):

        number = str(input_number)
        from_num_sys = int(from_num_sys)
        to_num_sys = int(to_num_sys)

        dot_index = number.find(',')
        _, iter_start, iter_end = self.get_iter_number_start_end(number)
        for index, power in enumerate(range(iter_start, iter_end, -1)):
            if index == dot_index:
                print(' ', end='')
            print(abs(power), end='')
        print(' <- exponents')

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
            if power_eval < 0:
                power_eval = f'({power_eval})'
            temp_term_list = split_term[:-1] + [str(power_eval)]
            term_term = ' '.join(temp_term_list)
            short_terms.append(term_term)
        short_expression = ' + '.join(short_terms)
        self.print_with_equality(short_expression)

        eval_terms = [eval(term) for term in short_terms]
        str_eval_terms = [str(term) if term >= 0 else str(f'({term})') for term in eval_terms]

        middle_expression = ' + '.join(str_eval_terms)
        self.print_with_equality(middle_expression, end=' ')

        result_number = sum(eval_terms)
        print(result_number)

        result_number = round(result_number, 5)
        return result_number

    @staticmethod
    def print_with_equality(expression: str, end='\n'):
        print('= %s =' % expression, end=end)

    def get_iter_number_start_end(self, number):
        split_number = number.split(',')
        if len(split_number) == 2:
            iter_number = split_number[0] + split_number[1]

            iter_start = len(split_number[0]) - 1
            iter_end = -(len(split_number[1]) + 1)
        else:
            iter_number = number

            iter_start = len(number) - 1
            iter_end = -1
        return iter_number, iter_start, iter_end

    def get_terms_expression_and_letter_flag(self, number, from_num_sys, second_run=False):
        terms = []

        iter_number, iter_start, iter_end = self.get_iter_number_start_end(number)

        for digit, index in zip(iter_number, range(iter_start, iter_end, -1)):
            small_term_brackets = '', ''
            if index < 0:
                small_term_brackets = '(', ')'
            small_term = f'^{small_term_brackets[0]}{index}{small_term_brackets[1]}'

            big_term_brackets = '', ''
            if from_num_sys <= 0:
                big_term_brackets = '(', ')'
            big_term = f' * {big_term_brackets[0]}{from_num_sys}{big_term_brackets[1]}{small_term}'

            if second_run:
                if digit.isalpha():
                    digit = self.letter_to_digit(digit)
                if digit == '0':
                    continue
                if index == 0:
                    big_term = ''
                if index == 1:
                    big_term = f' * {big_term_brackets[0]}{from_num_sys}{big_term_brackets[1]}'

            full_term = '%s%s' % (digit, big_term)
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


class PrintWatcher:
    def __init__(self):
        self.remembered: List[int] = list()

    def print_table(self, table_dict, table_key):
        if table_key not in self.remembered:
            for key, value in table_dict[table_key].items():
                print(key, value)
            self.remembered.append(table_key)


class ShortTranslator(AbstractTranslator, ABC):
    def __init__(self, print_watcher: PrintWatcher):
        self.base_to_res_tables: Dict[int, Dict[str, str]] = self.get_base_to_res_table()
        self.res_to_base_tables: Dict[int, Dict[str, str]] = self.get_res_to_base_table(self.base_to_res_tables)
        self.print_watcher = print_watcher

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
        self.print_watcher.print_table(self.base_to_res_tables, from_num_sys)

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
        self.print_watcher.print_table(self.base_to_res_tables, to_num_sys)

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


def get_tasks() -> Dict:
    task_reader: AbstractTaskReader = EasyTaskReader()
    tasks: Dict = task_reader.get_read_tasks()
    return tasks


def get_translators() -> Dict[int, AbstractTranslator]:
    print_whatcher = PrintWatcher()

    translators = {1: FromDecimalToAny(),
                   2: FromAnyToDecimal(),
                   3: FromAnyToAny(),
                   4: FromDecimalToAny(),
                   5: FromBigToSmallShort(print_whatcher),
                   6: FromBigToSmallShort(print_whatcher),
                   7: FromSmallToBigShort(print_whatcher),
                   8: FromAnyToDecimal(),
                   9: FromAnyToDecimal()}
    return translators


if __name__ == '__main__':
    translator = FromDecimalToAny()
    translator.translate('0,0025', 10, 16)
