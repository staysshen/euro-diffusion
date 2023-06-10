from typing import List, Dict, Any, Optional, Tuple


class Algorithm:

    # Порція монет, що використовується для поділу з сусідніми містами
    REPRESENTATIVE_PORTION: int = 1000

    # Початкова кількість монет у міста при створенні
    INITIAL_COIN_COUNT: int = 1000000

    def __init__(
            self,
            lines: List[str]
    ):

        # Список країн
        self.countries: List[Country] = []

        # Створення країн з переданими рядками
        self.create_countries(lines)

    def create_countries(self, lines: List[str]):
        # Створення країн з кожного рядка і додавання їх до списку країн

        self.countries = list(map(self.create_country_from_line, lines))

    @staticmethod
    def create_country_from_line(line: str) -> Any:

        # Розбиття рядка на елементи та створення об'єкта країни з відповідними параметрами
        name, xl, yl, xh, yh = line.split()

        return Country(name, int(xl), int(yl), int(xh), int(yh))

    def create_empty_world_map(self) -> List[List[None]]:

        # Визначення розмірів пустої області, що охоплює всі країни
        min_xl: int = min(country.xl for country in self.countries)
        min_yl: int = min(country.yl for country in self.countries)
        max_xh: int = max(country.xh for country in self.countries)
        max_yh: int = max(country.yh for country in self.countries)

        # Створення пустої області
        return [[None for _ in range(max_yh - min_yl + 1)] for _ in range(max_xh - min_xl + 1)]

    def create_cities(self, world_map: List[List[None]]) -> None:
        # Створення міст для кожної країни та розміщення їх у відповідній позиції на світовій карті

        # Знаходимо мінімальне значення xl серед усіх країн
        min_xl = min(country.xl for country in self.countries)

        # Знаходимо мінімальне значення yl серед усіх країн
        min_yl = min(country.yl for country in self.countries)

        # Проходимося по кожній країні
        for country in self.countries:

            # Проходимося по значенням xl, xh (включно) для поточної країни
            for i in range(country.xl, country.xh + 1):

                # Проходимося по значенням yl, yh (включно) для поточної країни
                for j in range(country.yl, country.yh + 1):
                    # Обчислюємо відносну позицію x для світової карти
                    x: int = i - min_xl

                    # Обчислюємо відносну позицію y для світової карти
                    y: int = j - min_yl

                    # Створюємо об'єкт міста для поточної країни
                    city = City(len(self.countries), self.countries.index(country))

                    # Розміщуємо місто на світовій карті за відповідною позицією
                    world_map[x][y] = city

                    # Додаємо місто до поточної країни
                    country.add_city(city)

    @staticmethod
    def set_neighbors(world_map: List[List[Any]]) -> None:

        # Отримуємо ширину та висоту світової карти
        width: int = len(world_map)
        height: int = len(world_map[0])

        def is_valid_coordinate(x: int, y: int) -> bool:
            # Перевіряємо, чи координати (x, y) є в межах світової карти

            return 0 <= x < width and 0 <= y < height

        def get_neighbor(x: int, y: int) -> Optional[Any]:
            # Отримуємо сусіда міста за координатами (x, y)

            return world_map[x][y] if is_valid_coordinate(x, y) else None

        for x, row in enumerate(world_map):
            for y, city in enumerate(row):
                if city:

                    # Отримуємо сусідів для поточного міста за допомогою сусідніх координат
                    neighbors: List[Optional[Any]] = [
                        get_neighbor(x + 1, y),
                        get_neighbor(x - 1, y),
                        get_neighbor(x, y + 1),
                        get_neighbor(x, y - 1)
                    ]

                    # Встановлюємо сусідів міста, виключаючи значення None
                    city.neighbors = [neighbor for neighbor in neighbors if neighbor]

    def initialize(self) -> None:
        # Ініціалізація алгоритму: створення пустої області, створення міст та додавання сусідів

        world_map: List[List[None]] = self.create_empty_world_map()

        self.create_cities(world_map)
        self.set_neighbors(world_map)

    def is_completed(self) -> bool:
        # Перевірка, чи всі країни завершили свій процес

        return all(country.is_completed() for country in self.countries)

    def validate_connectivity(self) -> bool:
        # Перевірка, чи всі країни взаємодосяжні

        # Ініціалізується за визначення досяжності до першої країни
        connected: List[Country] = [self.countries[0]]

        # Кількість обходів дорівнює кількості країн
        for _ in range(len(self.countries)):
            for country in self.countries:

                # Якщо країна вже визначена, як досяжна
                if country in connected:
                    pass

                # Співставлення країн, досяжних із першої
                for connected_country in connected:

                    # Визначення межування країн
                    if (
                            country.xl - connected_country.xh == 1 or
                            country.yl - connected_country.yh == 1 or
                            country.xh - connected_country.xl == -1 or
                            country.yh - connected_country.yl == -1
                    ):

                        connected.append(country)
                        break

        # Випадок, коли є недосяжні країни
        for country in self.countries:
            if country not in connected:
                return False

        # Випадок, коли немає недосяжних країн
        return True

    def run(self) -> Optional[List[Tuple[str, int]]]:

        def case_for_unreachable() -> [List[Tuple[str, int]]]:
            result: Dict[str, float] = {}
            for country in self.countries:
                result[country.name] = float('inf')

            print("Connections don't exist for some counties, so the goal will never be reached")

            return sorted(result.items(), key=lambda x: (x[1], x[0]))

        if not self.validate_connectivity():
            return case_for_unreachable()

        # Ініціалізація алгоритму
        self.initialize()

        # Словник з результатами країн
        result: Dict[str, int] = {}

        # Лічильник днів
        days: int = 0

        while True:
            for country in self.countries:
                for city in country.cities:
                    # Поділ монет з сусідніми містами
                    city.share_with_neighbors()

                if country.is_completed():

                    # Якщо країна завершила свій процес, додаємо її до результатів з поточною кількістю днів
                    if country.name not in result:
                        result[country.name] = days

            # Якщо всі країни завершили свій процес, виходимо з циклу
            if self.is_completed():
                break

            for country in self.countries:
                for city in country.cities:
                    # Оновлення стану міст
                    city.update()

            # Збільшуємо лічильник днів
            days += 1

        # Сортування результатів за кількістю днів та назвою країни
        return sorted(result.items(), key=lambda x: (x[1], x[0]))


class City:
    def __init__(
            self,
            country_count,
            country_index
    ):

        # Позначає, чи завершено обробку монет у місті
        self.completed: bool = False

        # Список сусідніх міст
        self.neighbors: List = []

        # Кількість країн
        self.country_count = country_count

        # Кількість монет для кожної країни
        self.coins: List[int] = [0] * country_count

        # Тимчасовий кеш для монет кожної країни
        self.cache: List[int] = [0] * country_count

        # Початкова кількість монет для країни міста
        self.coins[country_index] = Algorithm.INITIAL_COIN_COUNT

    def share_with_neighbors(self) -> None:

        # Якщо всі країни мають хоча б одну монету, вважаємо місто завершеним
        if all(coin_count > 0 for coin_count in self.coins):
            self.completed = True

        for index, coin_count in enumerate(self.coins):
            if coin_count >= Algorithm.REPRESENTATIVE_PORTION:
                share = coin_count // Algorithm.REPRESENTATIVE_PORTION

                # Поділ монети з сусідніми містами
                for city in self.neighbors:
                    city.cache[index] += share
                    self.coins[index] -= share

    def update(self) -> None:
        # Оновлення стану монет для кожної країни

        for i in range(self.country_count):
            self.coins[i] += self.cache[i]
            self.cache[i] = 0


class Country:
    def __init__(
            self,
            name: str,
            xl: int,
            yl: int,
            xh: int,
            yh: int
    ):
        # Назва країни
        self.name: str = name

        # Список міст у країні
        self.cities: List[City] = []

        # Мінімальне значення координати x для країни
        self.xl: int = xl

        # Мінімальне значення координати y для країни
        self.yl: int = yl

        # Максимальне значення координати x для країни
        self.xh: int = xh

        # Максимальне значення координати y для країни
        self.yh: int = yh

    def add_city(
            self,
            city: City
    ) -> None:
        # Додавання міста до країни

        self.cities.append(city)

    def is_completed(self) -> bool:
        # Перевірка, чи завершено обробку монет у всіх містах країни

        return all(city.completed for city in self.cities)
