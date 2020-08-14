from calendar import HTMLCalendar, day_abbr
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class EventCalendar(HTMLCalendar):

    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)
        self.cssclass_month = "table"
        self.cssclass = "table-primary"

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<th class="table-primary">%s</th>' % day_abbr[day]


    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if day in self.events:
                cssclass += ' filled'
                body = ['<ul>']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % event.get_absolute_url())
                    body.append(esc(event.place.name))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')


    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s" style="word-wrap: \
        break-word;min-width: 160px;max-width: 160px;"><small>%s</small></td>' % (cssclass, body)
