from models import Algorithm  # Імпортуємо клас Algorithm з модуля models

def run_algorithm(filename):
    tasks = []  # Створюємо порожній список для результатів

    with open(filename, 'r') as file:  # Відкриваємо файл для читання
        country_count = read_country_count(file)  # Зчитуємо кількість країн з першого рядка файлу

        while country_count:  # Виконуємо цикл, поки кількість країн не дорівнює 0
            if not 1 <= country_count <= 20:  # Перевіряємо, чи кількість країн задовільняє обмеження
                return None  # Повертаємо None, якщо кількість країн не в діапазоні [1, 20]

            lines = read_lines(file, country_count)  # Зчитуємо вхідні дані для кожної країни

            result = run_algorithm_for_lines(lines)  # Виконуємо алгоритм та отримуємо результат
            tasks.append(result)  # Зберігаємо результат у списку

            next_line = file.readline().strip()  # Зчитуємо наступний рядок файлу та видаляємо зайві пробіли
            if not next_line:  # Якщо рядок порожній, це означає закінчення файлу
                break  # Виходимо з циклу

            country_count = int(next_line)  # Оновлюємо значення кількості країн

    return tasks  # Повертаємо список результатів

def read_country_count(file):
    return int(file.readline())  # Зчитуємо кількість країн з першого рядка файлу

def read_lines(file, count):
    return [file.readline() for _ in range(count)]  # Зчитуємо вхідні дані для кожної країни

def run_algorithm_for_lines(lines):
    algorithm = Algorithm(lines)  # Створюємо екземпляр Algorithm зі зчитаними даними
    return algorithm.run()  # Запускаємо алгоритм

    #return tasks  # Повертаємо список результатів
