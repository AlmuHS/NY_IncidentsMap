import folium
import io

from query_incidents import QueryDF


class EditMap:
    def __init__(self, location: list):
        self.location = location
        self.map = folium.Map(location)

    def add_marker_to_map(self, latitude: float, longitude: float):
        folium.Marker([latitude, longitude]).add_to(self.map)

    def clean_map(self):
        self.map = None
        self.map = folium.Map(self.location)

    def export_map(self, mapobj: io):
        map_io = self.map.save(mapobj, close_file=False)

        return map_io


class QueryMap:
    def __init__(self, filename: str):
        self.file = filename
        self.query_tool = QueryDF(filename)
        self.map_edit = EditMap([40.541, -74.178])

    def _show_points_in_map(self, point_list: list):
        self.map_edit.clean_map()

        for i, point in point_list.iterrows():
            latitude = float(point['Latitude'])
            longitude = float(point['Longitude'])

            self.map_edit.add_marker_to_map(latitude, longitude)

        map_data = io.BytesIO()
        self.map_edit.export_map(map_data)

        return map_data

    def show_marks_by_neighborhood(self, nb_name: str):
        nb_ptr_df = self.query_tool.search_by_neighborhood(
            nb_name)

        self._show_points_in_map(nb_ptr_df)

    def show_marks_by_date(self, year: int, month: int):
        year_ptr_df = self.query_tool.search_by_date(year, month)
        map_data = self._show_points_in_map(year_ptr_df)

        return map_data

    def show_marks_by_neighborhood_and_date(self, nbh_name: str, year: int, month: int):
        ptr_df = self.query_tool.search_by_neighborhood_and_date(nbh_name,
                                                                 year, month)
        map_data = self._show_points_in_map(ptr_df)

        return map_data


query_tool = QueryMap('incidents.csv')
query_tool.show_marks_by_date(2018, 4)
query_tool.show_marks_by_date(2020, 4)
query_tool.show_marks_by_neighborhood('Gravesend-Sheepshead Bay')
query_tool.show_marks_by_neighborhood_and_date(
    'Gravesend-Sheepshead Bay', 2020, 6)
