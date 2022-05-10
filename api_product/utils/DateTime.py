from datetime import datetime


class DateTime:
    @classmethod
    def last_day_of_month(cls, year, month):
        last_days = [31, 30, 29, 28, 27]
        for i in last_days:
            try:
                end = datetime(year, month, i)
            except ValueError:
                continue
            else:
                return end.date().day
        return None
