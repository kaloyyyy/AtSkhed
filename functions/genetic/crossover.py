import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def crossover_generation(current_gen_crossover: int):
    print('Generating crossover...')
    tables = cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'offspring_{current_gen_crossover}%'").fetchall()
    last_table = tables[-1]['name']
    count = int(offspring_count / 2)
    i_rand = 0
    j_rand = 1
    while len(tables) > 1:

        i_rand = randint(0, len(tables) - 1)
        j_rand = randint(0, len(tables) - 1)
        while i_rand == j_rand:
            i_rand = randint(0, len(tables) - 1)
            j_rand = randint(0, len(tables) - 1)

        parent_1 = tables[i_rand]
        parent_2 = tables[j_rand]
        # print(len(tables), tables[i_rand]['name'], tables[j_rand]['name'])
        parent_names = [parent_1['name'], parent_2['name']]
        tables.remove(parent_1)
        tables.remove(parent_2)
        crossover(parent_1, parent_2, count, current_gen_crossover, parent_names)
        count += 2


def crossover(parent_1, parent_2, count, gen, parent_names):
    time_list = list(range(1, 67))
    cross_points = sample(time_list, int(multipoint_crossover_count))
    # new table select then paste paste
    table_name_1 = f'offspring_{gen}_{count}'
    table_name_2 = f'offspring_{gen}_{count + 1}'
    offspring_first = f'''CREATE TABLE IF NOT EXISTS {table_name_1} AS
                    SELECT time_id, class_id, classroom_id 
                    FROM {parent_1['name']}'''
    offspring_second = f'''CREATE TABLE IF NOT EXISTS {table_name_2} AS
                    SELECT time_id, class_id, classroom_id 
                    FROM {parent_2['name']}'''

    cursor.execute(offspring_first)
    cursor.execute(offspring_second)
    print(parent_1['name'], parent_2['name'])
    print(table_name_1, table_name_2)
    conn.commit()
    for x in cross_points:
        cut_from_1 = cursor.execute(f"select * from {table_name_1} where classroom_id = {x}").fetchall()
        cut_from_2 = cursor.execute(f"select * from {table_name_2} where classroom_id = {x}").fetchall()

        for row, row2 in zip(cut_from_1, cut_from_2):
            class_id_1 = row['class_id']
            class_id_2 = row2['class_id']
            if class_id_1 is None:
                class_id_1 = 'NULL'
            if class_id_2 is None:
                class_id_2 = 'NULL'

            update_1 = f"UPDATE {table_name_1} SET class_id = {class_id_2} where time_id = {row['time_id']} and classroom_id = {x}"
            cursor.execute(update_1)
            update_2 = f"UPDATE {table_name_2} SET class_id = {class_id_1} where time_id = {row2['time_id']} and classroom_id = {x}"
            cursor.execute(update_2)
    parental_reference_query = f"INSERT into parentals(parent_1, parent_2, child) values('{parent_names[0]}','{parent_names[1]}', '{table_name_1}')"
    cursor.execute(parental_reference_query)
    parental_reference_query = f"INSERT into parentals(parent_1, parent_2, child) values('{parent_names[0]}','{parent_names[1]}', '{table_name_2}')"
    cursor.execute(parental_reference_query)


if __name__ == '__main__':
    current_generation = 1
    crossover_generation(current_generation)
    conn.commit()
