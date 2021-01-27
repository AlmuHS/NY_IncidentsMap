import numpy as np

import psycopg2
from postgis.psycopg import register


class PostGISQuery:
    def setup_pg_connection(self):
        connection = psycopg2.connect(
            host="localhost", database="postgis_db", user="postgis_test", password="postgis")

        register(connection)
        self.cursor = connection.cursor()

        return self.cursor

    def send_query(self, query_str: str):
        self.cursor.execute(query_str)
        results = self.cursor.fetchall()

        return results


class CityQuery:
    def __init__(self, pg_query: PostGISQuery):
        self.pg_query = pg_query
        self.pg_query.setup_pg_connection()

    def search_neighborhood(self, coordinates_str: str):
        nyc_neighborhood = self.pg_query.send_query(
            f"select name from nyc_neighborhoods where ST_contains(geom, ST_Transform(ST_GeomFromText({coordinates_str}, 4326), 26918))")

        nyc_nb_filtered = nyc_neighborhood[0][0]

        return nyc_nb_filtered


class ProcessFile:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_file_data()

    def load_file_data(self):
        self.incidents_mat = np.genfromtxt(
            self.filename, dtype=object, delimiter='\t')

    def fill_incident_neighborhood(self):
        pg_connect = PostGISQuery()
        city_query = CityQuery(pg_connect)

        neighborhood_incident = []

        for incident in self.incidents_mat:
            longitude = incident[1].decode('utf-8')
            latitude = incident[2].decode('utf-8')

            coordinates_str = f"\'POINT({longitude} {latitude})\'"
            ny_nb = city_query.search_neighborhood(coordinates_str)

            neighborhood_incident.append(ny_nb)

        self.incidents_mat = np.insert(
            self.incidents_mat, 3, neighborhood_incident, axis=1)

        return self.incidents_mat

    def remove_day_from_date(self):
        for incident in self.incidents_mat:
            date = str(incident[0].decode('utf-8'))
            date_wo_day = date[:-3]

            incident[0] = date_wo_day
            incident[1] = incident[1].decode('utf-8')
            incident[2] = incident[2].decode('utf-8')

        return self.incidents_mat

    def export_to_csv(self, output_file: str):
        np.savetxt(output_file, self.incidents_mat,
                   delimiter=",", newline="\n", fmt="%s")


file_process = ProcessFile("incidents.txt")
incidents_mat = file_process.fill_incident_neighborhood()
incidents_mat = file_process.remove_day_from_date()
print(incidents_mat)
file_process.export_to_csv("incidents.csv")
