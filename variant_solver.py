from solvers import get_tasks, get_translators
from sys import argv
from pprint import pprint


def main():
    variant_number = int(argv[1]) if len(argv) == 2 else 1

    tasks = get_tasks()
    translators = get_translators()

    task_variant = tasks[variant_number]
    pprint(task_variant)
    print()

    max_task_number = max(translators.keys())
    for task_number in range(1, max_task_number + 1):
        print(f"Task #{task_number}")
        actual_task = task_variant[task_number]
        translator = translators[task_number]
        translator.translate(*actual_task)
        print()


if __name__ == '__main__':
    main()
