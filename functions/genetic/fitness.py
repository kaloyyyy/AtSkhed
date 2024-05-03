import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def evaluation_of_generation(generation: int):
    from functions import consecutive_conflict_class, first_to_last_class, check_consecutive
    tables = cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'offspring_{generation}%'").fetchall()
    # conflict_weight
    # long_break_weight
    # RLE_schedule_weight
    # classroom_preference_weight
    # first_to_last_class_weight
    # concurrent_course_weight
    # semester
    conflicts: list[int] = []
    long_breaks: list[int] = []
    long_class: list[int] = []
    seven_to_seven_class: list[int] = []
    conflict_consecutive_breaks: list[int] = []
    fitness_results = {}
    for table in tables:
        table_name = table['name']
        # print(table_name)
        conflict_consecutive_breaks = consecutive_conflict_class(table_name)

        conflicts.append(conflict_consecutive_breaks[0])
        long_class.append(conflict_consecutive_breaks[1])
        long_breaks.append(conflict_consecutive_breaks[2])
        seven_to_seven = first_to_last_class(table_name)
        seven_to_seven_class.append(seven_to_seven)
        fitness_results[table_name] = 0
    # fitness_results["yes"] = 0
    # conflicts.append(0)
    # long_class.append(0)
    # long_breaks.append(0)
    # seven_to_seven_class.append(0)
    norm_conflicts = normalize(conflicts, conflict_max, 'conflict_max')
    norm_long_class = normalize(long_class, consecutive_classes_max, 'consecutive_classes_max')
    norm_long_breaks = normalize(long_breaks, long_break_max, 'long_break_max')
    norm_seven_to_seven_class = normalize(seven_to_seven_class, first_to_last_class_max, 'first_to_last_class_max')

    for i, (x) in enumerate(fitness_results):
        fitness_results[x] = (conflict_weight * norm_conflicts[i]) + (long_break_weight * norm_long_breaks[i]) + (
                consecutive_classes_weight * norm_long_class[i] + (norm_seven_to_seven_class[i]*first_to_last_class_weight))
        fitness_results[x] = round(fitness_results[x], 8)
        # If the row does not exist, insert it
        update_fitness_table = f"INSERT OR REPLACE INTO fitness (offspring_table, fitness) VALUES ('{x}', '{fitness_results[x]}')"

        cursor.execute(update_fitness_table)
    conn.commit()

    sorted_fitness_results = sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)
    #  sorted_fitness_results is the sorted list of tuples
    sorted_fitness_results_dict = {k: v for k, v in sorted_fitness_results}

    print(sorted_fitness_results_dict)
    return sorted_fitness_results_dict


def normalize(data: list, constraint_max, setting_name) -> list:
    min_value = 0
    max_value = max(data)
    if max_value < constraint_max:
        max_value = constraint_max
    else:
        constraint_max = max_value
        cursor.execute(f"UPDATE settings SET setting_value = {constraint_max} WHERE setting_name = '{setting_name}'")
        conn.commit()
    if min_value == max_value:  # Handle identical values (avoid division by zero)
        return [1] * len(data)  # Return a list of ones
    return [round(100 - ((x - 0) / (max_value - 0)) * 100, 8) for x in data]


if __name__ == '__main__':
    evaluation_of_generation(65)
