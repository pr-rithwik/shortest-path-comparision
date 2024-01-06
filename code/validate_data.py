from code.constants import DOLLAR_SIGN
import sys


class DataValidator:
    def __init__(self, data_processor) -> None:
        self.data_processor = data_processor
        
        self.people_df = self.data_processor.people_df
        self.movies_df = self.data_processor.movies_df

        self.person_name_id_birth_map = self.data_processor.person_name_id_birth_map
        self.person_id_name_map = self.data_processor.person_id_name_map
        self.movie_id_name_map = self.data_processor.movie_id_name_map
    
    def validate_actor_names(self, from_actor_name, to_actor_name):
        from_actor_id = self.get_actor_id(from_actor_name)
        if from_actor_id is None:
            sys.exit("First Person not found.")
        
        to_actor_id = self.get_actor_id(to_actor_name)
        if to_actor_id is None:
            sys.exit("Second Person not found.")
        
        return from_actor_id, to_actor_id

    def get_actor_id(self, actor_name):
        actor_name = actor_name.lower().strip()

        try:
            if len(self.person_name_id_birth_map[actor_name]) == 1:
                id_detail = self.person_name_id_birth_map[actor_name][0]
                return id_detail.split(DOLLAR_SIGN)[0]
            else:
                return self.select_right_actor_id(actor_name)
        except:
            return None

    def select_right_actor_id(self, actor_name):
        person_ids = []
        for each in self.person_name_id_birth_map[actor_name]:
            id_, birth = each.split(self.column_connector)
            person_ids.append(id_)
            print(f"ID: {id_}, Name: {actor_name}, Birth: {birth}")
        
        person_id = input("Intended Person ID: ")
        return person_id if person_id in person_ids else None
