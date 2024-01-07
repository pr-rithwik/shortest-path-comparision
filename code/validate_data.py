import sys


class DataValidator:
    def __init__(self, solution) -> None:
        self.solution = solution
        self.data_processor = self.solution.processor
    
    def validate_actor_names(self):
        if self.solution.from_actor_id is None:
            sys.exit("First Person not found.")
        
        if self.solution.to_actor_id is None:
            sys.exit("Second Person not found.")
