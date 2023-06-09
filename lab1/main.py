# Імпортуємо функцію run_algorithm з модуля algorithm
from algorithm import run_algorithm
from typing import List, Tuple


def main(input_file_path: str) -> None:
    # Викликаємо функцію run_algorithm для обробки вхідного файлу 'input.txt' і отримання результатів
    tasks: List[Tuple[str, int]] = run_algorithm(input_file_path)

    # Перевіряємо, чи є результати (не є None або порожнім списком)
    if tasks:

        # Проходимо по кожному випадку результату, використовуючи enumerate для отримання порядкового номера case_num
        for case_num, result in enumerate(tasks, start=1):

            # Виводимо заголовок з номером випадку
            print(f'\nCase Number {case_num}')

            # Проходимо по кожній країні та кількості днів в результаті
            for country, days in result:

                # Виводимо ім'я країни та кількість днів
                print(f'{country} {days}')


if __name__ == '__main__':
    # Викликаємо головну функцію main, якщо файл виконується як самостійний скрипт

    main('input_2.txt')
