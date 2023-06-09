class Algorithm:
    REPRESENTATIVE_PORTION = 1000  # Порція монет, що використовується для поділу з сусідніми містами
    INITIAL_COIN_COUNT = 1000000  # Початкова кількість монет у міста при створенні

    def __init__(self, lines):
        self.countries = []  # Список країн
        self.create_countries(lines)  # Створення країн з переданими рядками

    def create_countries(self, lines):
        # Створення країн з кожного рядка і додавання їх до списку країн
        self.countries = list(map(self.create_country_from_line, lines))

    def create_country_from_line(self, line):
        # Розбиття рядка на елементи та створення об'єкта країни з відповідними параметрами
        name, xl, yl, xh, yh = line.split()
        return Country(name, int(xl), int(yl), int(xh), int(yh))

    def create_empty_world_map (self):
        # Визначення розмірів пустої області, що охоплює всі країни
        min_xl = min(country.xl for country in self.countries)
        min_yl = min(country.yl for country in self.countries)
        max_xh = max(country.xh for country in self.countries)
        max_yh = max(country.yh for country in self.countries)

        return [[None for _ in range(max_yh - min_yl + 1)] for _ in range(max_xh - min_xl + 1)]  # Створення пустої області

    def create_cities(self, world_map):
        # Створення міст для кожної країни та розміщення їх у відповідній позиції на світовій карті
        min_xl = min(country.xl for country in self.countries)  # Знаходимо мінімальне значення xl серед усіх країн
        min_yl = min(country.yl for country in self.countries)  # Знаходимо мінімальне значення yl серед усіх країн

        for country in self.countries:  # Проходимося по кожній країні
            for i in range(country.xl, country.xh + 1):  # Проходимося по значенням xl, xh (включно) для поточної країни
                for j in range(country.yl, country.yh + 1):  # Проходимося по значенням yl, yh (включно) для поточної країни
                    x = i - min_xl  # Обчислюємо відносну позицію x для світової карти
                    y = j - min_yl  # Обчислюємо відносну позицію y для світової карти

                    city = City(len(self.countries), self.countries.index(country))  # Створюємо об'єкт міста для поточної країни

                    world_map[x][y] = city  # Розміщуємо місто на світовій карті за відповідною позицією
                    country.add_city(city)  # Додаємо місто до поточної країни


    def set_neighbors(self, world_map):
        # Отримуємо ширину та висоту світової карти
        width = len(world_map)
        height = len(world_map[0])

        def is_valid_coordinate(x, y):
            # Перевіряємо, чи координати (x, y) є в межах світової карти
            return 0 <= x < width and 0 <= y < height

        def get_neighbor(x, y):
            # Отримуємо сусіда міста за координатами (x, y)
            return world_map[x][y] if is_valid_coordinate(x, y) else None

        for x, row in enumerate(world_map):
            for y, city in enumerate(row):
                if city:
                    # Отримуємо сусідів для поточного міста за допомогою сусідніх координат
                    neighbors = [
                        get_neighbor(x + 1, y),
                        get_neighbor(x - 1, y),
                        get_neighbor(x, y + 1),
                        get_neighbor(x, y - 1)
                    ]
                    # Встановлюємо сусідів міста, виключаючи значення None
                    city.neighbors = [neighbor for neighbor in neighbors if neighbor]


    def initialize(self):
        # Ініціалізація алгоритму: створення пустої області, створення міст та додавання сусідів
        world_map  = self.create_empty_world_map ()

        self.create_cities(world_map )
        self.set_neighbors(world_map )

    def is_completed(self):
        # Перевірка, чи всі країни завершили свій процес
        return all(country.is_completed() for country in self.countries)

    def run(self):
        self.initialize()  # Ініціалізація алгоритму
        result = {}  # Словник з результатами країн
        days = 0  # Лічильник днів

        max_iterations = 1000  # Максимальна допустима кількість ітерацій
        iteration_count = 0  # Лічильник ітерацій

        while iteration_count < max_iterations:
            for country in self.countries:
                for city in country.cities:
                    city.share_with_neighbors()  # Поділ монет з сусідніми містами
                if country.is_completed():
                    # Якщо країна завершила свій процес, додаємо її до результатів з поточною кількістю днів
                    if country.name not in result:
                        result[country.name] = days
            if self.is_completed():
                # Якщо всі країни завершили свій процес, виходимо з циклу
                break
            for country in self.countries:
                for city in country.cities:
                    city.update()  # Оновлення стану міст

            days += 1  # Збільшуємо лічильник днів
            iteration_count += 1

        if iteration_count == max_iterations:
            print("Увага: програма може зациклитися!")
            
        return sorted(result.items(), key=lambda x: (x[1], x[0]))  # Сортування результатів за кількістю днів та назвою країни
class City:
    def __init__(self, country_count, country_index):
        self.completed = False  # Позначає, чи завершено обробку монет у місті
        self.neighbors = []  # Список сусідніх міст
        self.country_count = country_count  # Кількість країн
        self.coins = [0] * country_count  # Кількість монет для кожної країни
        self.cache = [0] * country_count  # Тимчасовий кеш для монет кожної країни
        self.coins[country_index] = self.get_initial_coin_count()  # Початкова кількість монет для країни міста

    def share_with_neighbors(self):
        if all(coin_count > 0 for coin_count in self.coins):
            # Якщо всі країни мають хоча б одну монету, вважаємо місто завершеним
            self.completed = True

        for index, coin_count in enumerate(self.coins):
            if coin_count >= self.get_representative_portion():
                share = coin_count // self.get_representative_portion()

                for city in self.neighbors:
                    # Поділ монети з сусідніми містами
                    city.cache[index] += share
                    self.coins[index] -= share

    def update(self):
        for i in range(self.country_count):
            # Оновлення стану монет для кожної країни
            self.coins[i] += self.cache[i]
            self.cache[i] = 0

    @staticmethod
    def get_initial_coin_count():
        # Повертає початкову кількість монет для країни
        return Algorithm.INITIAL_COIN_COUNT

    @staticmethod
    def get_representative_portion():
        # Повертає розмір порції монети для поділу з сусідами
        return Algorithm.REPRESENTATIVE_PORTION


class Country:
    def __init__(self, name, xl, yl, xh, yh):
        self.name = name  # Назва країни
        self.cities = []  # Список міст у країні
        self.xl = xl  # Мінімальне значення координати x для країни
        self.yl = yl  # Мінімальне значення координати y для країни
        self.xh = xh  # Максимальне значення координати x для країни
        self.yh = yh  # Максимальне значення координати y для країни

    def add_city(self, city):
        # Додавання міста до країни
        self.cities.append(city)

    def is_completed(self):
        # Перевірка, чи завершено обробку монет у всіх містах країни
        return all(city.completed for city in self.cities)
