import os
import sys
from math import ceil

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *



def selection(generation):
    print(color.GREEN + f'Selection in generation {generation}' + color.END)
    from functions import evaluation_of_generation
    selected = {}
    losers = []

    to_select = evaluation_of_generation(generation)
    elitism_count = ceil(len(to_select) * elitism_percentage)
    top_chosen = int(elitism_count)
    not_chosen = dict(list(to_select.items())[top_chosen:])
    selected.update(dict(list(to_select.items())[:top_chosen]))
    # Assuming not_chosen is the dictionary

    # tournament
    tournament_count = int(ceil(tournament_percentage * offspring_count))
    for i in range(tournament_count):
        tournament = {}
        random_key_1 = choice(list(not_chosen.keys()))
        tournament.update({random_key_1: not_chosen[random_key_1]})
        not_chosen.pop(random_key_1)
        random_key_2 = choice(list(not_chosen.keys()))
        tournament.update({random_key_2: not_chosen[random_key_2]})
        not_chosen.pop(random_key_2)
        print(tournament, end=" winner: ")
        if tournament[random_key_1] > tournament[random_key_2]:
            print(random_key_1, tournament[random_key_1])
            selected.update({random_key_1: tournament[random_key_1]})
        else:
            print(random_key_2, tournament[random_key_2])
            selected.update({random_key_2: tournament[random_key_2]})
    not_chosen_items = list(not_chosen.items())  # Convert dictionary items to a list of tuples
    roulette_chosen = sample(not_chosen_items, int(offspring_count * roulette_percentage ))
    selected.update(roulette_chosen)

    print(f"selection {len(selected)}: {selected}")
    return selected


def selection_query(selected_tables: dict, current_generation: int):
    for i, key in enumerate(selected_tables.keys()):
        table_name = f"offspring_{current_generation + 1}_{i}"
        create_chromosome_table_query = f'''CREATE TABLE IF NOT EXISTS {table_name} AS
                    SELECT time_id, class_id, classroom_id 
                    FROM {key}'''

        cursor.execute(create_chromosome_table_query)

        parental_reference_query = f"INSERT into parentals(parent_1, child) values('{key}', '{table_name}')"
        cursor.execute(parental_reference_query)
    conn.commit()


if __name__ == '__main__':
    current_generation = 0
    selection_query(selection(0), current_generation)
