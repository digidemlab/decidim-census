import pytz

from dateutil.relativedelta import relativedelta

from datetime import datetime


class Dater(object):
    def now():
        return datetime.now(pytz.timezone('Europe/Stockholm'))

    def today():
        now = Dater.now()
        return datetime(now.year, now.month, now.day)

    def yesterday():
        return str(Dater.today() - relativedelta(day=1)).replace(
            ' 00:00:00', '')
