from decimal import Decimal
import folium
from folium.plugins import MarkerCluster

from .models import Place


class FoliumMap:

    def __init__(self, queryset):
        self.queryset = queryset

    def create_folium_map(self):
        spb_coordinates = [59.946288, 30.349214]
        events_map = folium.Map(location=spb_coordinates,
                                zoom_start=13,
                                tiles='Stamen Toner')

        marker_cluster = MarkerCluster().add_to(events_map)

        for adress in self.queryset:
            (lat, lon) = (adress.lon, adress.lat)
            place = Place.objects.filter(event__adress=adress.id).distinct()[0]
            link = "/place/{}".format(place.id)
            text = folium.Html("<a href='{}'>{}</a>".format(link, place.name), script=True)
            folium.Marker(
                location=(lon, lat),
                popup=folium.Popup(text),
                icon=folium.Icon(color='green')
            ).add_to(marker_cluster)
        events_map = events_map.get_root().render()
        return events_map
