import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now() if not date
            else dt.datetime.strptime(date, '%d.%m.%Y')
        ).date()
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0

        for record in self.records:
            if record.date == dt.datetime.now().date():
                today_stats += record.amount

        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()

        for record in self.records:
            if 0 <= (today - record.date).days < 7:
                week_stats += record.amount

        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Получает остаток калорий на сегодня"""
        remain = self.limit - self.get_today_stats()

        if remain > 0:
            return (
                f'Сегодня можно съесть что-нибудь'
                f' ещё, но с общей калорийностью не более {remain} кКал'
            )
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0  # Курс доллар США.
    EURO_RATE = 70.0  # Курс Евро.

    def get_today_cash_remained(self, currency):
        currency_type = ''
        cash_remained = self.limit - self.get_today_stats()

        if currency == 'usd':
            cash_remained /= self.USD_RATE
            currency_type = 'USD'
        elif currency == 'eur':
            cash_remained /= self.EURO_RATE
            currency_type = 'Euro'
        elif currency == 'rub':
            currency_type = 'руб'

        if cash_remained > 0:
            round_cash_remained = round(cash_remained, 2)
            return (
                f'На сегодня осталось {round_cash_remained} '
                f'{currency_type}'
            )
        if cash_remained == 0:
            return 'Денег нет, держись'

        debt = -cash_remained
        return 'Денег нет, держись:' \
               ' твой долг - {:.2f} {}'.format(debt, currency_type)


def main():
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др",
                                      date="08.11.2019"))
    print(cash_calculator.get_today_cash_remained("rub"))


if __name__ == "__main__":
    main()
