import subprocess
import sys

from AtSKhed.settings import BASE_DIR
from config import *
from functions import *
from functions.genetic.mutation import mutation

# TODO:
#        Nursing Query RLE pls pls
#       Classroom type identities
#       Classroom location
#       Classroom Cap counter
#       Classroom Preferences and Requirements
#       RLE huuuur


GENERATIONS = 1
POPULATION_SIZE = 20


@timeit
def genetic_algorithm():
    global offspring_count, generation_count, mutation_rate
    from functions import drop_offsprings, initialize_offspring, initialize_sections, assign_section_to_class, check_conflicts, check_consecutive,check_long_break
    from functions import create_chromosome, init_fitness_table, selection_query, crossover_generation, selection, evaluation_of_generation, recurring_courses
    drop_offsprings()
    initialize_offspring()
    initialize_sections()
    assign_section_to_class()
    combine_algorithm()
    assign_room_to_class()
    conn.commit()
    cursor.execute("DELETE from parentals")
    cursor.execute("DELETE from fitness")
    conn.commit()
    int(offspring_count)

    for i in range(int(offspring_count)):
        create_chromosome(0, i)
    evaluation_of_generation(0)
    for j in range(int(generation_count)):
        print(j)
        selection_query(selection(j), j) #no +1 since previous
        crossover_generation(j+1)
        chance = random()
        print("mutation chance", chance)
        if mutation_rate >= chance:
            offspring_number = randint(0, int(offspring_count)-1)
            offspring_table = f"offspring_{j+1}_{offspring_number}"
            print(offspring_table)
            mutation(offspring_table)
        if mutation_rate*1.5 >= chance:
            offspring_number = randint(0, int(offspring_count)-1)
            offspring_table = f"offspring_{j+1}_{offspring_number}"
            print(offspring_table)
            tabu_search(offspring_table)
        if mutation_rate*1.5 >= chance:
            offspring_number = randint(0, int(offspring_count)-1)
            offspring_table = f"offspring_{j+1}_{offspring_number}"
            print(offspring_table)
            hillclimb(offspring_table)

        tabu_search(f"offspring_{j+1}_{int(offspring_count-1)}")
        hillclimb(f"offspring_{j+1}_{int(offspring_count-1)}")
        evaluation_of_generation(j+1)

    recurring_courses(f'offspring_0_{0}')

    conn.commit()


if __name__ == '__main__':
    genetic_algorithm()

    conn.commit()
    conn.close()
