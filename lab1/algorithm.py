# Імпортуємо клас Algorithm з модуля models
from typing import List, Optional, Any, Tuple

from models import Algorithm


def run_algorithm(filename: str) -> Optional[List[Tuple[str, int]]]:

    # Створюємо порожній список для результатів
    tasks: List[Tuple[str, int]] = []

    # Відкриваємо файл для читання
    with open(filename, 'r') as file:
        # Зчитуємо кількість країн з першого рядка файлу
        country_count: int = read_country_count(file)

        # Виконуємо цикл, поки кількість країн не дорівнює 0
        while country_count:

            # Перевіряємо, чи кількість країн задовільняє обмеження
            if not 1 <= country_count <= 20:

                # Повертаємо None, якщо кількість країн не в діапазоні [1, 20]
                return None

            # Зчитуємо вхідні дані для кожної країни
            lines: List[str] = read_lines(file, country_count)

            # Виконуємо алгоритм та отримуємо результат
            result = run_algorithm_for_lines(lines)

            # Зберігаємо результат у списку
            tasks.append(result)

            # Зчитуємо наступний рядок файлу та видаляємо зайві пробіли
            next_line: str = file.readline().strip()

            # Якщо рядок порожній, це означає закінчення файлу
            if not next_line:

                # Виходимо з циклу
                break

            # Оновлюємо значення кількості країн
            country_count: int = int(next_line)

    # Повертаємо список результатів
    return tasks


def read_country_count(file) -> int:
    # Зчитуємо кількість країн з першого рядка файлу

    return int(file.readline())


def read_lines(file, count) -> List[str]:
    # Зчитуємо вхідні дані для кожної країни

    return [file.readline() for _ in range(count)]


def run_algorithm_for_lines(lines) -> Optional[List[Tuple[str, int]]]:

    # Створюємо екземпляр Algorithm зі зчитаними даними
    algorithm: Algorithm = Algorithm(lines)

    # Запускаємо алгоритм
    return algorithm.run()

    # Повертаємо список результатів
    # return tasks
