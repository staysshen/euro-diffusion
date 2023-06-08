from models import Algorithm  # Імпортуємо клас Algorithm з модуля models

def run_algorithm(filename):
    tasks = []  # Створюємо порожній список для результатів

    with open(filename, 'r') as file:  # Відкриваємо файл для читання
        country_count = int(file.readline())  # Зчитуємо кількість країн з першого рядка файлу

        while country_count:  # Виконуємо цикл, поки кількість країн не дорівнює 0
            if not 1 <= country_count <= 20:  # Перевіряємо, чи кількість країн задовільняє обмеження
                return None  # Повертаємо None, якщо кількість країн не в діапазоні [1, 20]

            lines = [file.readline() for _ in range(country_count)]  # Зчитуємо вхідні дані для кожної країни

            algorithm = Algorithm(lines)  # Створюємо екземпляр Algorithm зі зчитаними даними
            tasks.append(algorithm.run())  # Запускаємо алгоритм та зберігаємо результат у списку

            next_line = file.readline().strip()  # Зчитуємо наступний рядок файлу та видаляємо зайві пробіли
            if not next_line:  # Якщо рядок порожній, це означає закінчення файлу
                break  # Виходимо з циклу

            country_count = int(next_line)  # Оновлюємо значення кількості країн

    return tasks  # Повертаємо список результатів
