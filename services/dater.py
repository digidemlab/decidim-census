import pytz

from dateutil.relativedelta import relativedelta

from datetime import datetime


class Dater(object):
    def now():
        return datetime.now(pytz.timezone('Europe/Stockholm'))

    def today():
        now = Dater.now()
        return str(datetime(now.year, now.month,
                            now.day)).replace(' 00:00:00', '')

    def yesterday():
        return Dater.today() + relativedelta(day=-1)
