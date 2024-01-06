from networkx import NetworkXNoPath
import networkx as nx

from .process_data import DataProcessor
from .validate_data import DataValidator
from .constants import DIRECTORY, PATH_CONNECTOR


class Solution():
    def __init__(self, from_actor, to_actor) -> None:
        self.processor = DataProcessor(DIRECTORY)
        self.from_actor = from_actor
        self.to_actor = to_actor

    def get_shortest_path(self, from_actor_id, to_actor_id):
        try:
            return nx.bidirectional_shortest_path(self.processor.G, from_actor_id, to_actor_id)
        except NetworkXNoPath:
            return None
    
    def process_output(self, path):
        people = [self.processor.person_id_name_map[each] for each in path[::2]]
        movies = [self.processor.movie_id_name_map[each] for each in path[1::2]]
    
        if path is None:
            print(f"There is NO PATH between {self.from_actor} and {self.to_actor}.")
        else:
            degree = len(path) // 2
            
            path = PATH_CONNECTOR.join(
                [f"{people[i]}{PATH_CONNECTOR}{movies[i]}" for i in range(degree)])
            path += f"{PATH_CONNECTOR}{self.to_actor}"
            
            print(f"The path is: {path}")
            print(f"The degree of separation is: {degree}")

def main():  
    from_actor, to_actor = "Cary Elwes", "Jack Nicholson"
    # from_actor, to_actor = input("First Name: "), input("Second Name: ")

    solution = Solution(from_actor, to_actor)
    solution.processor.load_data()
    solution.processor.update_map_details()
    
    validator = DataValidator(data_processor=solution.processor)
    from_actor_id, to_actor_id = validator.validate_actor_names(from_actor, to_actor)
    
    path = solution.get_shortest_path(from_actor_id, to_actor_id)
    
    solution.process_output(path)


if __name__ == "__main__":
    main()