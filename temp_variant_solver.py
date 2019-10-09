from solvers import get_tasks, get_translators
from sys import argv
from pprint import pprint
from typing import Dict, List


def main():
    variant_number = int(argv[1]) if len(argv) == 2 else 1

    print(f'Variant #{variant_number}')

    tasks = get_tasks()
    translators = get_translators()

    task_variant: Dict = tasks[variant_number]
    max_task_number = max(translators.keys())

    lens: List[int] = list()
    for i in range(0, 3):
        temp_len = len(max(task_variant.items(), key=lambda x: len(x[1][i]))[1][i])
        lens.append(temp_len)

    head: Dict[str, int] = dict()
    task_number_str = 'Task #'
    head[task_number_str] = len(task_number_str)

    for index, char in enumerate(['A', 'B', 'C']):
        head[char] = lens[index]

    for head_key, head_value in head.items():
        print('{:>{}}'.format(head_key, head_value), end='\t')
    print()

    for task_key in range(len(task_variant)):
        task_value = task_variant[task_key + 1]
        print('{:>{}}'.format(task_key + 1, head['Task #']), end='\t')

        for head_len_key, task_elem in zip(['A', 'B', 'C'], task_value):
            print('{:>{}}'.format(task_elem, head[head_len_key]), end='\t')
        print()

    print()

    answers = list()
    for task_number in range(1, max_task_number + 1):
        print(f"Task #{task_number}")
        actual_task = task_variant[task_number]
        translator = translators[task_number]
        answer = translator.translate(*actual_task)
        answers.append(answer)
        print()

    answer_str = 'Answer'
    head[answer_str] = len(answer_str)

    for head_key, head_value in head.items():
        print('{:>{}}'.format(head_key, head_value), end='\t')
    print()


if __name__ == '__main__':
    main()
