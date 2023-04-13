import json
import datetime

# Singleton патерн
class Customer:
    _instance = None

    def __new__(cls, name, surname):    # інстанс класу створиться лише за умови, що його не існує
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name, surname):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self.name = name
        self.surname = surname

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError('The name can not be empty!')
        self.__name = value

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        if not value:
            raise ValueError('The surname can not be empty!')
        self.__surname = value

    def __str__(self):
        return f'{self.name} {self.surname}'


class Order:
    def __init__(self, customer):
        self.day = datetime.datetime.now().weekday()
        self.pizza = pizza_by_day[self.day]
        self.customer = customer
        self.extra_items = []
        self.extra_price = 0
        self.total_price = 0

    def add_extra_item(self, ingredient):
        with open('pizza.json') as f:
            pizza = json.load(f)
        if ingredient not in pizza['ingredients']:
            raise KeyError(f'There is no {ingredient} in menu')
        if len(self.extra_items) >= 3:  # якщо довжина масиву >= 3, то масив більше не розширюємо
            raise ValueError('You can not add more than 3 extra ingredients')
        self.extra_items.append(ingredient)
        self.extra_price += pizza["ingredients"][ingredient]
        f.close()

    def get_total_price(self):
        return self.pizza.price + self.extra_price

    # join() у наступній функції виконує роль аналогічну implode у PHP
    def __str__(self):
        return f'\nOrder for {self.customer}' \
               f'\n{self.pizza}' \
               f'\nExtra: {", ".join(self.extra_items) if self.extra_items else "nothing"} - {self.extra_price} UAH' \
               f'\nTotal price - {float(self.get_total_price())} UAH' # тип int у тип float за допомогою float()


# батьківський клас
class MondayPizza:
    def __init__(self, day='0'):    # конструктор класу
        with open('pizza.json') as f:
            pizza = json.load(f)
        self.day = day
        self.name = pizza['pizza-of-the-day'][self.day]['name']
        self.price = pizza['pizza-of-the-day'][self.day]['price']
        self.ingredients = pizza['pizza-of-the-day'][self.day]['ingredients']
        f.close()

    def __str__(self):
        return f'Pizza {self.name} - {self.price} UAH'


# клас-нащадок
class TuesdayPizza(MondayPizza):
    def __init__(self):
        super().__init__('1')   # використання конструктора батьківського класу

# клас-нащадок
class WednesdayPizza(MondayPizza):
    def __init__(self):
        super().__init__('2')   # використання конструктора батьківського класу

# клас-нащадок
class ThursdayPizza(MondayPizza):
    def __init__(self):
        super().__init__('3')   # використання конструктора батьківського класу

# клас-нащадок
class FridayPizza(MondayPizza):
    def __init__(self):
        super().__init__('4')   # використання конструктора батьківського класу

# клас-нащадок
class SaturdayPizza(MondayPizza):
    def __init__(self):
        super().__init__('5')   # використання конструктора батьківського класу

# клас-нащадок
class SundayPizza(MondayPizza):
    def __init__(self):
        super().__init__('6')   # використання конструктора батьківського класу


# словник у Python виконує функцію хеш-масиву
pizza_by_day = {
    0: MondayPizza(),
    1: TuesdayPizza(),
    2: WednesdayPizza(),
    3: ThursdayPizza(),
    4: FridayPizza(),
    5: SaturdayPizza(),
    6: SundayPizza()
}


def main():
    try:
        client = Customer('Paul', 'Blanc')
        new_client = Customer('Pedro', 'Pascal')
        print(f'First client: {client} \nNew client: {new_client}') # два однакові імені, бо Customer - singleton
        order = Order(client)
        olive, chicken, mozzarella = 'olive', 'chicken', 'mozzarella'
        extra_string = olive + ',' + chicken + ',' + mozzarella         # розіменування змінних і конкатенація рядків
        extra = extra_string.split(',')                                 # функція split(), аналог explode у PHP
        for ingredient in extra:    # for проходить через всі значення масиву, аналогічно до forEach у PHP
            try:
                order.add_extra_item(ingredient)
            except KeyError as err:
                print(err.args[0])
    except ValueError as err:
        print(err)
    else:
        print(order)


main()
