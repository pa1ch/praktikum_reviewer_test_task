import datetime as dt  # из модуля datetime тебе нужен только один класс datetime, поэтому, чтобы писать меньше кода
# и не импортировать лишнее, лучше заменить твой импорт вот так: from datetime import datetime as dt
# тогда например твоя строка dt.datetime.now() изменится на более лаконичную dt.now()


class Record:
    def __init__(self, amount, comment, date=''):  # стоит добавить аннотацию типов переменных
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())  # можно разделить на две части: всё, что до else и всё остальное, начиная с else
        self.comment = comment  # лучше поменять присваивание comment и date, чтобы всё было последовательно и наглядно


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:  # Record - это имя класса. В цикле мы должны использовать переменную, имена переменных начинаются с маленькой буквы
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount  # можно записать кратко с помощью +=
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and  # можно записать всё проще: 0 <= (today - record.date).days < 7
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # из названия метода понятно, что он делает, лучше не оставлять очевидные комментарии, чтобы не засорять код
        # но если всё таки нужно оставить комментарий к методу, то стоит это делать с помощью Docsting
        # можешь почитать об этом тут https://peps.python.org/pep-0257/
        x = self.limit - self.get_today_stats()  # не стоит использовать однобуквенные названия переменных, это непонятно. Можно заменить например на remains
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \  # не применяем бэкслеши для переноса строки
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')  # лишние скобки


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    # очевидные комментарии
    # можно использовать int, если всё таки нужен float, то можно написать 60.0

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):  # не нужно передавать курс валют в метод, ты можешь им пользоваться и так
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00  # оператор двойного равно сравнивает значения переменных и возвращает True или
            # False. Чтобы присвоить значение какой-нибудь переменной, нужно использовать один знак равно
            currency_type = 'руб'
        if cash_remained > 0:  # для удобства чтения, стоит добавить сверху пустую строку для разделения сплошного кода на отдельные блоки
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '  # округлить стоит заранее, до формирования строки 
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \  # не применяем бэкслеши для переноса строки
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)  # тут можно использовать f-строки

    def get_week_stats(self):
        super().get_week_stats()
