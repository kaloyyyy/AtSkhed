import sys
import os

import numpy as np

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *

global update_offspring_table_query, check_room_query, offspring_table


def create_chromosome(generation, populationNumber):

    print(color.BLUE + f"Creating Chromosome {generation}_{populationNumber}", end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print('.', end='')
    time.sleep(0.5)
    print(f'.{color.END}', end=' ')
    time.sleep(0.5)
    global check_room_query, offspring_table, update_offspring_table_query
    offspring_table = f'offspring_{generation}_{populationNumber}'
    update_offspring_table_query = f'UPDATE {offspring_table} SET class_id = ? WHERE time_id = ? AND classroom_id = ?'
    check_room_query = (f'select * from {offspring_table} where classroom_id = ? and time_id >= ? and time_id <= ? '
                        f'and class_id not null')
    create_chromosome_table_query = f'''create table if not exists {offspring_table}
                                (
                                    time_id       int
                                        constraint offspring_timeSlots_time_id_fk
                                            references time_slots,
                                    class_id     integer
                                        constraint offspring_classes_class_id_fk
                                            references classes,
                                    classroom_id integer
                                        constraint offspring_classrooms_classroom_id_fk
                                            references classrooms,
                                    constraint offspring_pk
                                        primary key (time_id, classroom_id)
                                );'''
    cursor.execute(create_chromosome_table_query)
    cursor.execute(f'delete from {offspring_table}')
    initialize_table_query = f'''insert into {offspring_table} (time_id, class_id, classroom_id) 
                                select time_id, class_id, classroom_id from offspring;'''
    cursor.execute(initialize_table_query)

    for row in CLASS_RES:

        class_id_current = row['class_id']
        classroom_id = row['classroom_id']
        assign_section_res = cursor.execute(select_assign_section_query, (class_id_current,)).fetchone()
        if assign_section_res:
            units = assign_section_res['units']
            program = assign_section_res['program_name']
            code = assign_section_res['code']
            day_selector = None
            done = False
            get_classroom_query = f'select classroom_id from main.classes where class_id = {class_id_current}'
            classroom_id = cursor.execute(get_classroom_query).fetchone()['classroom_id']
            count_try = 0
            section_id = assign_section_res['section_id']
            if program == 'BS Nursing':
                pick_time_query = f"""SELECT ts.time_id
                                    FROM {offspring_table}
                                    JOIN main.time_slots ts ON ts.time_id = {offspring_table}.time_id
                                    WHERE class_id IS NULL
                                    AND classroom_id = {classroom_id}
                                    AND day IN (1, 2, 5, 6)
                                    AND ts.time_id NOT IN (
                                        SELECT time_id
                                    FROM RLE_schedule
                                    WHERE section_id = {section_id}
                                    )"""
            else:
                pick_time_query = f"""select ts.time_id
                                                    from {offspring_table}
                                                join main.time_slots ts on ts.time_id = {offspring_table}.time_id
                                                where class_id is null
                                                and classroom_id = {classroom_id} and day in (1,2,5,6)"""
            pick_time_results = cursor.execute(pick_time_query).fetchall()
            pick_list = [row["time_id"] for row in pick_time_results]

            while not done:
                count_try += 1
                # print(count_try, class_id_current, classroom_id)
                if count_try > 50 and classroom_id > 62:
                    classroom_id_new = np.random.randint(63, 69)
                    update_class_query = "update classes set classroom_id = ? where main.classes.class_id = ?"
                    cursor.execute(update_class_query, (classroom_id_new, class_id_current))
                    pick_time_query = f"""select ts.time_id
                                                from {offspring_table}
                                            join main.time_slots ts on ts.time_id = {offspring_table}.time_id
                                            where class_id is null
                                            and classroom_id = {classroom_id} and day in (1,2,5,6)"""
                    pick_time_results = cursor.execute(pick_time_query).fetchall()
                    pick_list = [row["time_id"] for row in pick_time_results]
                    count_try = 0
                    classroom_id = classroom_id_new
                # remove some time_slots in friday and saturday
                if len(pick_list) > 0:
                    if 40 in pick_list:
                        pick_list.remove(40)
                    if 48 in pick_list:
                        pick_list.remove(48)
                    # PATHFIT classes
                    if classroom_id > 62:
                        # print(class_id_current, time_pick_id, classroom_id)
                        to_remove = [7, 8, 23, 24, 39, 40]
                        for num in to_remove:
                            if num in pick_list:
                                pick_list.remove(num)
                    time_pick_id = int(np.random.choice(pick_list))
                    if time_pick_id <= 32:
                        day_selector = 1
                    elif 33 <= time_pick_id <= 47:
                        day_selector = 3
                    # Call the offspring_class_assignment function
                    done = offspring_class_assignment(class_id_current, time_pick_id, classroom_id, day_selector)
                    # print(offspring_table, time_pick_id, class_id_current, classroom_id)
                    pick_list.remove(time_pick_id)
                else:
                    # print("NEW TIME SET")
                    pick_time_query = f"""select ts.time_id
                                                from {offspring_table}
                                            join main.time_slots ts on ts.time_id = {offspring_table}.time_id
                                            where class_id is null
                                            and classroom_id = {classroom_id} and day in (1,2,5,6)"""
                    pick_time_results = cursor.execute(pick_time_query).fetchall()
                    pick_list = [row["time_id"] for row in pick_time_results]


    conn.commit()
    print(f'Offspring {generation}_{populationNumber} done' + color.END)


def offspring_class_assignment(class_id_current: int, time_pick_id: int, classroom_id: int, day: int) -> bool:
    global check_room_query, offspring_table

    if classroom_id > 62:
        if 7 <= time_pick_id <= 8 or 23 <= time_pick_id <= 24 or 39 <= time_pick_id <= 40 or day == 3:
            return False

        check_room_result_first = cursor.execute(check_room_query,
                                                 (classroom_id, time_pick_id, time_pick_id + 1)).fetchall()
        check_room_result_second = cursor.execute(check_room_query,
                                                  (classroom_id, time_pick_id + 16, time_pick_id + 17)).fetchall()

        if len(check_room_result_first) == 0:
            cursor.executemany(update_offspring_table_query, (
                (class_id_current, time_pick_id, classroom_id),
                (class_id_current, time_pick_id + 1, classroom_id)
            ))
            return True
        elif len(check_room_result_second) == 0:
            cursor.executemany(update_offspring_table_query, (
                (class_id_current, time_pick_id + 16, classroom_id),
                (class_id_current, time_pick_id + 17, classroom_id)
            ))
            return True
        else:
            return False

    if day == 1 or day == 2:
        check_room_result_first = cursor.execute(check_room_query,
                                                 (classroom_id, time_pick_id, time_pick_id)).fetchone()
        check_room_result_second = cursor.execute(check_room_query,
                                                  (classroom_id, time_pick_id + 16, time_pick_id + 16)).fetchone()
        if (check_room_result_first is None) and (check_room_result_second is None):
            cursor.executemany(update_offspring_table_query, (
                (class_id_current, time_pick_id, classroom_id),
                (class_id_current, time_pick_id + 16, classroom_id)
            ))
            return True
        else:
            return False
    elif day == 3 or day == 4:

        check_room_result = cursor.execute(check_room_query,
                                           (classroom_id, time_pick_id, time_pick_id + 1)).fetchall()
        if len(check_room_result) == 0:
            cursor.executemany(update_offspring_table_query, (
                (class_id_current, time_pick_id, classroom_id),
                (class_id_current, time_pick_id + 1, classroom_id)
            ))
            return True
        else:
            return False
    else:
        return False


def is_RLE_time(section_id):
    ...






if __name__ == '__main__':
    create_chromosome(0, 0)
    conn.commit()