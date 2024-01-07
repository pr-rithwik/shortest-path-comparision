import timeit
from unittest.mock import patch
from code.solution import main as run_solution
from code.constants import DIVIDING_OUTPUT_LINE


def get_actors():
    return [
        ("Cary Elwes", "Jack Nicholson"),
        # ("Quang Trung", "Elizabeth Bellak"),
        ("Oleg Stefan", "Danny Steg")
    ]

def test_bidirectional_shortest_path():
    actor_pairs = get_actors()
    for each_pair in actor_pairs:
        with patch('code.solution.get_actor_names') as mock_get:
            mock_get.return_value = each_pair
            run_solution()

def function_2():
    pass

def function_3():
    pass

functions = [test_bidirectional_shortest_path]

total_time = 0
examples_count = len(get_actors())
print(f"Testing on {examples_count} examples: ")
print(DIVIDING_OUTPUT_LINE)
print(DIVIDING_OUTPUT_LINE)

for func in functions:
    execution_time = timeit.timeit(func, number=1) / examples_count
    total_time += execution_time
    # print(f"{func.__name__} - Execution Time: {execution_time:.6f} seconds")

print(f"{func.__name__} - Average Total Time: {total_time:.6f} seconds")
