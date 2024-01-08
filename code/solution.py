from networkx import NetworkXNoPath
import networkx as nx

from . import DataProcessor, DataValidator
from .constants import (
    DIRECTORY, PATH_CONNECTOR, DIVIDING_OUTPUT_LINE, TEXT_GREEN_COLOR,
    TEXT_YELLOW_COLOR, TEXT_DEFAULT_COLOR, DOLLAR_SIGN
)


class Solution():
    def __init__(self, from_actor, to_actor) -> None:
        self.processor = DataProcessor(DIRECTORY)
        self.from_actor = from_actor
        self.to_actor = to_actor

        self.from_actor_id = None
        self.to_actor_id = None

        self.load_data()
        self.update_actor_ids(from_actor, to_actor)

    def load_data(self):
        self.processor.load_data()
        self.processor.update_map_details()

    def update_actor_ids(self, from_actor=None, to_actor=None):
        if from_actor is not None:
            self.from_actor = from_actor
            self.from_actor_id = self._get_actor_id(from_actor)
        
        if to_actor is not None:
            self.to_actor = to_actor
            self.to_actor_id = self._get_actor_id(to_actor)

    def get_shortest_path(self):
        try:
            return nx.bidirectional_shortest_path(
                self.processor.G, self.from_actor_id, self.to_actor_id)
        except NetworkXNoPath:
            return None
    
    def get_djikstra_shortest_path(self):
        try:
            return nx.dijkstra_path(
                self.processor.G, self.from_actor_id, self.to_actor_id)
        except NetworkXNoPath:
            return None

    def get_bidirectional_djikstra_shortest_path(self):
        try:
            return nx.bidirectional_dijkstra(
                self.processor.G, self.from_actor_id, self.to_actor_id)[1]
        except NetworkXNoPath:
            return None

    def get_bellman_ford_path(self):
        try:
            return nx.bellman_ford_path(
                self.processor.G, self.from_actor_id, self.to_actor_id)
        except NetworkXNoPath:
            return None

    def process_output(self, path):
        if path is None:
            print(f"There is NO PATH between {self.from_actor} and {self.to_actor}.")
            print(DIVIDING_OUTPUT_LINE)
        else:
            people = [self.processor.person_id_name_map[each] for each in path[::2]]
            movies = [self.processor.movie_id_name_map[each] for each in path[1::2]]

            colors = [TEXT_GREEN_COLOR, TEXT_YELLOW_COLOR]
            reset_color = TEXT_DEFAULT_COLOR
            degree = len(path) // 2
            
            path = PATH_CONNECTOR.join(
                [f"{colors[0]}{people[i]}{reset_color}{PATH_CONNECTOR}{colors[1]}{movies[i]}{reset_color}" for i in range(degree)])
            path += f"{PATH_CONNECTOR}{colors[0]}{self.to_actor}{reset_color}"
            
            print(f"The degree of separation between {colors[0]}{people[0]} & {people[-1]}{reset_color}: {degree}")
            print(f"The path is: {path}")
            print(DIVIDING_OUTPUT_LINE)

    def _get_actor_id(self, actor_name):
        actor_name = actor_name.lower()
        actor_id_detail = self.processor.get_actor_id_detail(actor_name)
        if len(actor_id_detail) == 1:
            actor_id = actor_id_detail[0]["actor_id"]
        else:
            actor_id = self._select_right_actor_id(actor_name)
        
        return actor_id

    def _select_right_actor_id(self, actor_name):
        person_ids = []
        for each in self.person_name_id_birth_map[actor_name]:
            id_, birth = each.split(DOLLAR_SIGN)
            person_ids.append(id_)
            print(f"ID: {id_}, Name: {actor_name}, Birth: {birth}")
        
        person_id = input("Intended Person ID: ")
        return person_id if person_id in person_ids else None


def get_actor_names():
    return input("First Name: "), input("Second Name: ")

def get_solution_func(solution):
    function_map = {
        "shortest_path": solution.get_shortest_path,
        "djikstra_path": solution.get_djikstra_shortest_path,
        "bidirectional_djikstra_path": solution.get_bidirectional_djikstra_shortest_path,
        "bellman_ford_path": solution.get_bellman_ford_path
    }
    
    return function_map["bellman_ford_path"]

def main():
    # from_actor, to_actor = get_actor_names() 
    from_actor, to_actor = "Cary Elwes", "Jack Nicholson"

    solution = Solution(from_actor, to_actor)

    validator = DataValidator(solution=solution)
    validator.validate_actor_names()
    
    solution_func = get_solution_func(solution)
    path = solution_func()

    solution.process_output(path)


if __name__ == "__main__":
    main()