import pandas as pd


class QueryDF:
    def __init__(self, filename: str = None, df: pd.DataFrame = None):
        if filename:
            self.incidents_df = self.load_data(filename)
        else:
            self.incidents_df = df

    def load_data(self, filename: str):
        self.incidents_df = pd.read_csv(filename)
        self.incidents_df.columns = [
            "Date", "Longitude", "Latitude", "Neighborhood"]

        self.incidents_df["Date"] = pd.to_datetime(self.incidents_df["Date"])

        return self.incidents_df

    def get_neighborhood_list(self):
        nb_list = self.incidents_df["Neighborhood"].drop_duplicates()
        nb_list.sort_values(inplace=True)
        nb_list = nb_list.tolist()

        return nb_list

    def search_by_date_range(self, date_start: str, date_end: str):
        date_end = pd.to_datetime(date_end)
        date_start = pd.to_datetime(date_start)

        query_date = self.incidents_df.loc[(self.incidents_df["Date"] >= date_start) & (
            self.incidents_df["Date"] <= date_end)]

        date_list = query_date["Date"].drop_duplicates()
        date_list.sort_values(inplace=True)
        date_list = date_list.tolist()

        return query_date, date_list

    def search_by_date(self, date_str: str):
        date = pd.to_datetime(date_str)

        query_date = self.incidents_df.loc[(self.incidents_df["Date"] == date)]

        num_inc = len(query_date)

        return query_date, num_inc

    def search_by_neighborhood(self, nbh_name: str):
        query_nb = self.incidents_df.loc[self.incidents_df["Neighborhood"] == nbh_name]

        num_inc = len(query_nb)

        return query_nb, num_inc

    def search_by_neighborhood_and_date_range(self, nbh_name: str, date_start: str, date_end: str):
        date_end = pd.to_datetime(date_end)
        date_start = pd.to_datetime(date_start)

        query = self.incidents_df.loc[(self.incidents_df["Neighborhood"] == nbh_name) & (
            self.incidents_df["Date"] >= date_start) & (self.incidents_df["Date"] <= date_end)]

        date_list = query["Date"].drop_duplicates()
        date_list.sort_values(inplace=True)
        date_list = date_list.tolist()

        return query, date_list
