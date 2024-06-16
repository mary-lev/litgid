from decimal import Decimal
import folium
from folium.plugins import MarkerCluster
import xyzservices.providers as xyz
from django.conf import settings



class FoliumMap:

    def __init__(self, queryset):
        self.queryset = queryset

    def create_folium_map(self):
        spb_coordinates = [59.946288, 30.349214]
        events_map = folium.Map(location=spb_coordinates,
                                zoom_start=13,
                                )
        tile_provider = xyz.Stadia.StamenToner

        # Update the URL to include the API key placeholder
        tile_provider["url"] = tile_provider["url"] + f"?api_key={settings.TILES_API_KEY}"

        folium.TileLayer(
            tiles=tile_provider.build_url(api_key=settings.TILES_API_KEY),
            attr=tile_provider.attribution,
            name=tile_provider.name,
            max_zoom=tile_provider.max_zoom,
            detect_retina=True
        ).add_to(events_map)
        #folium.LayerControl().add_to(events_map)

        marker_cluster = MarkerCluster().add_to(events_map)

        for adress in self.queryset:
            link = "/place/{}".format(adress['event__place__id'])
            text = folium.Html("<a href='{}'>{}</a>".format(
                link, adress['event__place__name']), script=True)
            folium.Marker(
                location=(adress['lat'], adress['lon']),
                popup=folium.Popup(text),
                icon=folium.Icon(color='green')
            ).add_to(marker_cluster)
        events_map = events_map.get_root().render()
        return events_map
