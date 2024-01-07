import timeit
from code.solution import Solution
from code.validate_data import DataValidator
from code.constants import DIVIDING_OUTPUT_LINE


def get_actors():
    return [
        ("Cary Elwes", "Jack Nicholson"),
        ("Quang Trung", "Elizabeth Bellak"),
        ("Oleg Stefan", "Danny Steg")
    ]


def test_bidirectional_shortest_path():
    actor_pairs = get_actors()
    
    for each_pair in actor_pairs:
        solution = Solution(*each_pair)
        
        validator = DataValidator(solution=solution)
        validator.validate_actor_names()
        
        path = solution.get_shortest_path()
        solution.process_output(path)

def test_djikstra_shortest_path():
    actor_pairs = get_actors()
    for each_pair in actor_pairs:
        solution = Solution(*each_pair)
        
        validator = DataValidator(solution=solution)
        validator.validate_actor_names()
        
        path = solution.get_djikstra_shortest_path()
        solution.process_output(path)


def test_bidirectional_djikstra_shortest_path():
    actor_pairs = get_actors()
    for each_pair in actor_pairs:
        solution = Solution(*each_pair)
        
        validator = DataValidator(solution=solution)
        validator.validate_actor_names()
        
        path = solution.get_bidirectional_djikstra_shortest_path()
        solution.process_output(path)


def main():
    functions = [
        test_bidirectional_shortest_path,
        test_djikstra_shortest_path,
        test_bidirectional_djikstra_shortest_path
    ]

    examples_count = len(get_actors())
    print(f"Testing on {examples_count} examples: ")
    print(DIVIDING_OUTPUT_LINE)
    print(DIVIDING_OUTPUT_LINE)

    for func in functions:
        execution_time = timeit.timeit(func, number=1) / examples_count
        print(f"{func.__name__} - Average Total Time: {execution_time:.4f} seconds")
        print(DIVIDING_OUTPUT_LINE)
        print(DIVIDING_OUTPUT_LINE)


if __name__ == "__main__":
    main()