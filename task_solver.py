from solvers import get_tasks, get_translators, AbstractTranslator
from sys import argv


def main():
    task_number = int(argv[1]) if len(argv) == 2 else 1

    tasks = get_tasks()
    translators = get_translators()

    translator: AbstractTranslator = translators[task_number]
    for variant_value in tasks.values():
        actual_task: list = variant_value[task_number]

        translator.translate(*actual_task)
        print()


if __name__ == '__main__':
    main()
