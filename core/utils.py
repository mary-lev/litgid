from calendar import HTMLCalendar, day_abbr
from itertools import groupby
from django.utils.html import conditional_escape as esc
import folium
from decimal import Decimal

from .models import Place, Adress

month_name = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']


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
                    body.append('<a href="%s">' % event
                        .get_absolute_url())
                    body.append(esc(event.place.name))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''
                    .join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonthname(self, year, month, withyear=True):
        """
        Return a month name as a table row.
        """
        current_month = '%s %s' % (month_name[month-1], year)
        return '<tr><th colspan="7" class="display-4"><center>%s</center></th></tr>' % (current_month)

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s" style="word-wrap: break-word;min-width: \
                160px;max-width: 160px;"><small>%s</small></td>' % (cssclass, body)

    def previous_month(self, year, month):
        if self.month == 1:
            previous_month = 12
            previous_year = self.year-1
        else:
            previous_year = self.year
            previous_month = self.month-1
        result = {'year': previous_year, 'month': previous_month, 'name': month_name[previous_month-1]}
        return result

    def next_month(self, year, month):
        if self.month == 12:
            next_month = 1
            next_year = self.year+1
        else:
            next_month = self.month+1
            next_year = self.year
        result = {'year': next_year, 'month': next_month, \
                'name': month_name[next_month-1]}
        return result


class FoliumMap():

    def __init__(self, queryset):
        self.queryset = queryset

    def create_folium_map(self, **kwargs):
        spb_coordinates = [59.946288, 30.349214]
        m = folium.Map(location=spb_coordinates,
            zoom_start=13,
            tiles='Stamen Toner')

        for all in self.queryset:
            (lat, lon) = (all.coordinates.replace('[', '').
                replace(']', '')
                .split(', '))
            place = Place.objects.filter(event__adress=all.id).distinct()[0]
            link = "/place/{}".format(place.id)
            text = folium.Html("<a href='{}'>{}</a>".format(link, place.name), script=True)
            folium.Marker(
                location= (lon, lat),
                popup=folium.Popup(text),
                icon=folium.Icon(color='green')
                ).add_to(m)
        m = m.get_root().render()
        return m