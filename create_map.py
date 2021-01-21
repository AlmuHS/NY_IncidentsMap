import pandas as pd
import folium
import folium.plugins
import io

from query_incidents import QueryDF


class EditMap:
    def __init__(self, location: list):
        self.location = location
        self.map = folium.Map(location, zoom_start=200)

    def create_markercluster(self):
        self.marker_cluster = folium.plugins.MarkerCluster().add_to(self.map)

    def add_marker_to_cluster(self, latitude: float, longitude: float):
        folium.Marker([latitude, longitude]).add_to(self.marker_cluster)

    def add_marker_to_map(self, latitude: float, longitude: float):
        folium.Marker([latitude, longitude]).add_to(self.map)

    def clean_map(self):
        self.map = None
        self.map = folium.Map(self.location)

    def fit_map_zoom(self, pnt_min: pd.DataFrame, pnt_max: pd.DataFrame):
        self.map.fit_bounds([pnt_min, pnt_max])

    def export_map(self, mapobj: io):
        map_io = self.map.save(mapobj, close_file=False)

        return map_io


class QueryMap:
    def __init__(self, filename: str = None, df: pd.DataFrame = None):
        if filename:
            self.file = filename
            self.query_tool = QueryDF(filename=filename)
        else:
            self.query_tool = QueryDF(df=df)

        self.map_edit = EditMap([40.541, -74.178])

    def _calculate_min_point(self, point_list: list):
        min_pnt = point_list[['Latitude',
                              'Longitude']].min().values.tolist()

        return min_pnt

    def _calculate_max_point(self, point_list: list):
        max_pnt = point_list[['Latitude',
                              'Longitude']].max().values.tolist()

        return max_pnt

    def _show_points_in_map(self, point_list: list):
        if len(point_list) > 0:
            latitude = float(point_list['Latitude'].iloc[0])
            longitude = float(point_list['Longitude'].iloc[0])

            self.map_edit = EditMap([latitude, longitude])
            self.map_edit.create_markercluster()

            for i, point in point_list.iterrows():
                latitude = float(point['Latitude'])
                longitude = float(point['Longitude'])

                self.map_edit.add_marker_to_cluster(latitude, longitude)

            min_pnt = self._calculate_min_point(point_list)
            max_pnt = self._calculate_max_point(point_list)

            self.map_edit.fit_map_zoom(min_pnt, max_pnt)

        else:
            self.map_edit.clean_map()

        map_data = io.BytesIO()
        self.map_edit.export_map(map_data)

        return map_data

    def show_marks_by_neighborhood(self, nb_name: str):
        nb_ptr_df, num_inc = self.query_tool.search_by_neighborhood(
            nb_name)
        map_data = self._show_points_in_map(nb_ptr_df)

        return map_data, num_inc

    def show_marks_by_date(self, date_str: str):
        date_ptr_df, num_inc = self.query_tool.search_by_date(date_str)

        map_data = self._show_points_in_map(date_ptr_df)

        return map_data, num_inc

    def show_marks_by_date_range(self, date_start: str, date_end: str):
        date_ptr_df, date_list = self.query_tool.search_by_date_range(
            date_start, date_end)

        map_iterator = MapIterator(date_ptr_df, date_list)

        return map_iterator

    def show_marks_by_neighborhood_and_date_range(self, nbh_name: str, date_start: str, date_end: str):
        pts_df, date_list = self.query_tool.search_by_neighborhood_and_date_range(
            nbh_name, date_start, date_end)

        map_iterator = MapIterator(pts_df, date_list)

        return map_iterator

    def show_map(self):
        map_data = io.BytesIO()
        self.map_edit.export_map(map_data)

        return map_data


class MapIterator:
    def __init__(self, query_df: pd.DataFrame, date_list: list):
        self.query_df = query_df
        self.date_list = date_list
        self.index = 0
        self.end = False

    def show_reg(self):
        query_tool = QueryMap(df=self.query_df)

        if self.date_list and (self.index in range(0, len(self.date_list))):
            date = self.date_list[self.index]
        else:
            date = 0
            self.end = True

        map_data, num_inc = query_tool.show_marks_by_date(date)

        return map_data, num_inc, date

    def show_next_reg(self):
        if self.index < len(self.date_list)-1:
            self.index += 1
            self.end = False

        map_data, num_inc, date = self.show_reg()

        if self.index == len(self.date_list)-1:
            self.end = True

        return map_data, num_inc, date, self.end

    def show_back_reg(self):

        if self.index >= 0:
            self.index -= 1
            self.end = False

        map_data, num_inc, date = self.show_reg()

        if self.index == 0:
            self.end = True

        return map_data, num_inc, date, self.end
