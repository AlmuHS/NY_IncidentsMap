import pandas as pd
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
    def __init__(self, filename: str = None, df: pd.DataFrame = None):
        if filename:
            self.file = filename
            self.query_tool = QueryDF(filename=filename)
        else:
            self.query_tool = QueryDF(df=df)

        self.map_edit = EditMap([40.541, -74.178])

    def _show_points_in_map(self, point_list: list):
        latitude = float(point_list['Latitude'].iloc[0])
        longitude = float(point_list['Longitude'].iloc[0])

        self.map_edit = EditMap([latitude, longitude])

        for i, point in point_list.iterrows():
            latitude = float(point['Latitude'])
            longitude = float(point['Longitude'])

            self.map_edit.add_marker_to_map(latitude, longitude)

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

    def show_reg(self):
        query_tool = QueryMap(df=self.query_df)

        if self.date_list:
            date = self.date_list[self.index]
        else:
            date = 0

        map_data, num_inc = query_tool.show_marks_by_date(date)

        return map_data, num_inc, date

    def show_next_reg(self):
        if self.index < len(self.date_list)-1:
            self.index += 1
        map_data, num_inc, date = self.show_reg()

        return map_data, num_inc, date

    def show_back_reg(self):
        if self.index > 0:
            self.index -= 1
        map_data, num_inc, date = self.show_reg()

        return map_data, num_inc, date
