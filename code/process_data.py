import networkx as nx
import pandas as pd

from .constants import DOLLAR_SIGN, PERSON_PREFIX, MOVIE_PREFIX, \
    PEOPLE_FILE_NAME, MOVIES_FILE_NAME, STARS_FILE_NAME


class DataProcessor:
    def __init__(self, directory) -> None:
        self.directory = directory
        
        self.people_df = None
        self.movies_df = None
        self.stars_df = None

        self.G = nx.Graph()
    
        self.person_name_id_birth_map = None
        self.person_id_name_map = None
        self.movie_id_name_map = None        

    def load_data(self):
        self.people_df = self.get_people_details()
        self.movies_df = self.get_movie_details()
        self.stars_df = self.get_stars_details()
        
        self.G.add_nodes_from(self.people_df["id"])
        self.G.add_nodes_from(self.movies_df["id"])
        self.G.add_edges_from(nx.from_pandas_edgelist(
            self.stars_df, "person_id", "movie_id").edges)
            
    def update_map_details(self):
        self.person_id_name_map = dict(zip(self.people_df.id, self.people_df.name))
        
        self.people_df["name_lower"] = self.people_df["name"].apply(
            lambda x: x.lower().strip())
        self.people_df["id_birth"] = self.people_df.apply(
            lambda x: f"{x['id']}{DOLLAR_SIGN}{x['birth']}", axis=1)
        self.person_name_id_birth_map = \
            self.people_df.groupby('name_lower')["id_birth"].apply(list)
        
        self.movie_id_name_map = dict(zip(self.movies_df.id, self.movies_df.title))

    def get_people_details(self):
        people_df = pd.read_csv(f"{self.directory}/{PEOPLE_FILE_NAME}")
        people_df["id"] = people_df["id"].apply(
            lambda x: f"{PERSON_PREFIX}{x}")
        
        return people_df

    def get_movie_details(self):
        movies_df = pd.read_csv(f"{self.directory}/{MOVIES_FILE_NAME}")
        movies_df["id"] = movies_df["id"].apply(
            lambda x: f"{MOVIE_PREFIX}{x}")

        return movies_df

    def get_stars_details(self):
        stars_df = pd.read_csv(f"{self.directory}/{STARS_FILE_NAME}")
        stars_df["person_id"] = stars_df["person_id"].apply(
            lambda x: f"{PERSON_PREFIX}{x}")
        stars_df["movie_id"] = stars_df["movie_id"].apply(
            lambda x: f"{MOVIE_PREFIX}{x}")
        
        return stars_df
    
    def get_actor_id_detail(self, actor_name):
        id_details = []
        for each in self.person_name_id_birth_map[actor_name]:
            id_, year = each.split(DOLLAR_SIGN)
            id_details.append({"actor_id": id_, "year": year})

        return id_details