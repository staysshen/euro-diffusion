from algorithm import run_algorithm  # Імпортуємо функцію run_algorithm з модуля algorithm

def main():
    tasks = run_algorithm('input.txt')  # Викликаємо функцію run_algorithm для обробки вхідного файлу 'input.txt' і отримання результатів
    if tasks:  # Перевіряємо, чи є результати (не є None або порожнім списком)
        for case_num, result in enumerate(tasks, start=1):  # Проходимо по кожному випадку результату, використовуючи enumerate для отримання порядкового номера case_num
            print(f'\nCase Number {case_num}')  # Виводимо заголовок з номером випадку
            for country, days in result:  # Проходимо по кожній країні та кількості днів в результаті
                print(f'{country} {days}')  # Виводимо ім'я країни та кількість днів

if __name__ == '__main__':
    main()  # Викликаємо головну функцію main, якщо файл виконується як самостійний скрипт
