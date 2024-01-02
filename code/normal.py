import networkx as nx
from networkx import NetworkXNoPath
import pandas as pd
import sys


class Solution:
    def __init__(self, directory) -> None:
        self.directory = directory
        self.person_name_id_birth_map = None
        self.person_id_name_map = None
        self.movie_id_name_map = None
        
        self.G = nx.Graph()
        
        self.column_connector = "$"
        self.person_id_prefix = "P-"
        self.movie_id_prefix = "M-"

        self.people_file_name = "people.csv"
        self.movies_file_name = "movies.csv"
        self.stars_file_name = "stars.csv"
        
    def load_data(self):
        people_df = self.get_people_details()
        self.person_id_name_map = dict(zip(people_df.id, people_df.name))
        self.person_name_id_birth_map = \
            people_df.groupby('name_lower')["id_birth"].apply(list)

        movies_df = self.get_movie_details()
        self.movie_id_name_map = dict(zip(movies_df.id, movies_df.title))

        stars_df = self.get_stars_details()
        
        self.G.add_nodes_from(people_df["id"])
        self.G.add_nodes_from(movies_df["id"])
        self.G.add_edges_from(nx.from_pandas_edgelist(
            stars_df, "person_id", "movie_id").edges)
    
    def get_actor_id(self, actor_name):
        actor_name = actor_name.lower().strip()

        try:
            if len(self.person_name_id_birth_map[actor_name]) == 1:
                id_detail = self.person_name_id_birth_map[actor_name][0]
                return id_detail.split(self.column_connector)[0]
            else:
                return self.select_right_actor_id(actor_name)
        except:
            return None

    def get_shortest_path(self, from_actor, to_actor):
        try:
            return nx.bidirectional_shortest_path(self.G, from_actor, to_actor)
        except NetworkXNoPath:
            return None

    def get_people_details(self):
        people_df = pd.read_csv(f"{self.directory}/{self.people_file_name}")
        people_df = people_df.astype(str)
        
        people_df["id"] = people_df["id"].apply(
            lambda x: f"{self.person_id_prefix}{x}")
        people_df["name_lower"] = people_df["name"].apply(
            lambda x: x.lower().strip())
        people_df["id_birth"] = people_df.apply(
            lambda x: f"{x['id']}{self.column_connector}{x['birth']}", axis=1)
        
        return people_df

    def get_movie_details(self):
        movies_df = pd.read_csv(f"{self.directory}/{self.movies_file_name}")
        movies_df["id"] = movies_df["id"].apply(
            lambda x: f"{self.movie_id_prefix}{x}")

        return movies_df

    def get_stars_details(self):
        stars_df = pd.read_csv(f"{self.directory}/{self.stars_file_name}")
        stars_df["person_id"] = stars_df["person_id"].apply(
            lambda x: f"{self.person_id_prefix}{x}")
        stars_df["movie_id"] = stars_df["movie_id"].apply(
            lambda x: f"{self.movie_id_prefix}{x}")
        
        return stars_df

    def select_right_actor_id(self, actor_name):
        person_ids = []
        for each in self.person_name_id_birth_map[actor_name]:
            id_, birth = each.split(self.column_connector)
            person_ids.append(id_)
            print(f"ID: {id_}, Name: {actor_name}, Birth: {birth}")
        
        person_id = input("Intended Person ID: ")
        return person_id if person_id in person_ids else None


def main():  
    directory = "large"
    
    solution = Solution(directory)
    solution.load_data()

    from_actor, to_actor = "Cary Elwes", "Jack Nicholson"

    # from_actor = input("Name: ")
    from_actor_id = solution.get_actor_id(from_actor)
    if from_actor_id is None:
        sys.exit("Person not found.")
    
    # to_actor = input("Name: ")
    to_actor_id = solution.get_actor_id(to_actor)
    if to_actor_id is None:
        sys.exit("Person not found.")

    path = solution.get_shortest_path(from_actor_id, to_actor_id)
    people = [solution.person_id_name_map[each] for each in path[::2]]
    movies = [solution.movie_id_name_map[each] for each in path[1::2]]
    
    if path is None:
        print(f"There is NO PATH between {from_actor} and {to_actor}.")
    else:
        path_joiner = " -> "
        degree = len(path) // 2
        
        path = path_joiner.join(
            [f"{people[i]}{path_joiner}{movies[i]}" for i in range(degree)])
        path += f"{path_joiner}{to_actor}"
        
        print(f"The path is: {path}")
        print(f"The degree of separation is: {degree}")


if __name__ == "__main__":
    main()