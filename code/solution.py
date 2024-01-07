from networkx import NetworkXNoPath
import networkx as nx

from .process_data import DataProcessor
from .validate_data import DataValidator
from .constants import DIRECTORY, PATH_CONNECTOR, DIVIDING_OUTPUT_LINE


class Solution():
    def __init__(self, from_actor, to_actor) -> None:
        self.processor = DataProcessor(DIRECTORY)
        self.from_actor = from_actor
        self.to_actor = to_actor

    def run_solution(self):
        self.processor.load_data()
        self.processor.update_map_details()

    def get_shortest_path(self, from_actor_id, to_actor_id):
        try:
            return nx.bidirectional_shortest_path(self.processor.G, from_actor_id, to_actor_id)
        except NetworkXNoPath:
            return None
    
    def process_output(self, path):
        if path is None:
            print(f"There is NO PATH between {self.from_actor} and {self.to_actor}.")
        else:
            people = [self.processor.person_id_name_map[each] for each in path[::2]]
            movies = [self.processor.movie_id_name_map[each] for each in path[1::2]]

            colors = ["\033[92m", "\033[93m"]
            reset_color = "\033[0m"
            degree = len(path) // 2
            
            path = PATH_CONNECTOR.join(
                [f"{colors[0]}{people[i]}{reset_color}{PATH_CONNECTOR}{colors[1]}{movies[i]}{reset_color}" for i in range(degree)])
            path += f"{PATH_CONNECTOR}{colors[0]}{self.to_actor}{reset_color}"
            
            print(f"The degree of separation between {colors[0]}{people[0]} & {people[-1]}{reset_color}: {degree}")
            print(f"The path is: {path}")
            print(DIVIDING_OUTPUT_LINE)

def get_actor_names():
    return input("First Name: "), input("Second Name: ")

def main():
    from_actor, to_actor = get_actor_names() 
    # from_actor, to_actor = "Cary Elwes", "James Dean"

    solution = Solution(from_actor, to_actor)
    solution.processor.load_data()
    solution.processor.update_map_details()
    
    validator = DataValidator(data_processor=solution.processor)
    from_actor_id, to_actor_id = validator.validate_actor_names(from_actor, to_actor)
    
    path = solution.get_shortest_path(from_actor_id, to_actor_id)
    
    solution.process_output(path)


if __name__ == "__main__":
    main()