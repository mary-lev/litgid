"""Все переписать на базе класса TextCalendar,
чтобы убрать отсюда форматирование таблицы для шаблона."""
from calendar import HTMLCalendar, TextCalendar, day_abbr
from itertools import groupby
from django.utils.html import conditional_escape as esc

from .models import Event

month_name = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']


class Test_Calendar(TextCalendar):

    def __init__(self, year, month):
        super().__init__()
        self.year = year
        self.month = month

    def collect_events(self):
        weeks = [week for week in self.monthdays2calendar(self.year, self.month)]
        weeks_with_events = list()
        for week in weeks:
            new_week = list()
            for day in week:
                if day[0] != 0 and day[1] != 0:
                    events = Event.objects.filter(
                        date__year=self.year,
                        date__month=self.month,
                        date__day=day[0]
                        ).count()
                    new_week.append((day, events))
                else:
                    new_week.append((day, 0))
            weeks_with_events.append(new_week)
        return weeks_with_events
