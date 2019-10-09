from solvers import get_tasks, get_translators
from sys import argv
from pprint import pprint


def main():
    variant_number = int(argv[1]) if len(argv) == 2 else 1
    print(f'Variant {variant_number}')

    tasks = get_tasks()
    translators = get_translators()

    task_variant = tasks[variant_number]
    task_format = '{:>6} {:>11} {:>2} {:>3}'
    print(task_format.format('Task #', 'A', 'B', 'C'))
    for task_key in range(1, len(task_variant) + 1):
        print(task_format.format(task_key, *task_variant[task_key]))
    print()

    answers = list()
    max_task_number = max(translators.keys())
    for task_number in range(1, max_task_number + 1):
        print(f"Task #{task_number}")
        actual_task = task_variant[task_number]
        translator = translators[task_number]
        answer = translator.translate(*actual_task)
        answers.append(answer)
        print()

    task_format += ' {:>14}'
    print(task_format.format('Task #', 'A', 'B', 'C', 'Answer'))
    for task_key in range(1, max_task_number + 1):
        print(task_format.format(task_key, *task_variant[task_key], answers[task_key - 1]))
    print()


if __name__ == '__main__':
    main()
