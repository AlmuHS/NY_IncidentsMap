import pandas as pd


class QueryDF:
    def __init__(self, filename: str):
        self.incidents_df = self.load_data(filename)

    def load_data(self, filename: str):
        self.incidents_df = pd.read_csv(filename)
        self.incidents_df.columns = [
            "Date", "Longitude", "Latitude", "Neighborhood"]

        return self.incidents_df

    def _get_date_str(self, year: int, month: int):
        if month < 10:
            month_str = f"0{month}"
        else:
            month_str = f"{month}"

        date_str = f"{year}-{month_str}"

        return date_str

    def search_by_date(self, year: int, month: int):
        date_str = self._get_date_str(year, month)
        query_date = self.incidents_df.loc[self.incidents_df["Date"] == date_str]

        return query_date

    def search_by_neighborhood(self, nbh_name: str):
        query_nb = self.incidents_df.loc[self.incidents_df["Neighborhood"] == nbh_name]

        return query_nb

    def search_by_neighborhood_and_date(self, nbh_name: str, year: int, month: int):
        date_str = self._get_date_str(year, month)
        query = self.incidents_df.loc[(self.incidents_df["Neighborhood"] == nbh_name) & (
            self.incidents_df["Date"] == date_str)]

        return query
