import sys
import os

from functions import consecutive_conflict_class

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def mutation(offspring_table):
    from functions import consecutive_conflict_class
    print(color.RED + f'Mutation {offspring_table}' + color.END)
    global check_room_query, update_offspring_table_query, table_name
    table_name = offspring_table
    update_offspring_table_query = f'UPDATE {table_name} SET class_id = ? WHERE time_id = ? AND classroom_id = ?'
    check_room_query = (f'select * from {table_name} where classroom_id = ? and time_id >= ? and time_id <= ? '
                        f'and class_id not null')
    classroom_list = list(range(1, 63))
    day_selector = -1
    mutation_points = sample(classroom_list, int(mutation_change_point))
    for point in mutation_points:
        select_column = f"select * from {offspring_table} where class_id is not NULL and classroom_id = {point}"
        vacant_time_select = f"""select {offspring_table}.time_id from {offspring_table} 
                                    join main.time_slots ts on ts.time_id = {offspring_table}.time_id 
                                    where class_id IS NULL and classroom_id = {point}"""
        not_null_result = cursor.execute(select_column).fetchall()
        vacant_results = cursor.execute(vacant_time_select).fetchall()
        taken_list_class = [row['class_id'] for row in not_null_result]
        vacant_list = [row['time_id'] for row in vacant_results]

        print(vacant_list)
        print(point, vacant_list)
        if len(vacant_list) > 0:
            if 40 in vacant_list:
                vacant_list.remove(40)
            if 48 in vacant_list:
                vacant_list.remove(48)

            if point > 62:
                # print(class_id_current, time_pick_id, classroom_id)
                to_remove = [7,8,23,24,39,40]
                for num in to_remove:
                    if num in vacant_list:
                        vacant_list.remove(num)
        select_count = 0
        if len(vacant_list) > mutation_change_point:
            select_count = int(len(vacant_list))

        if vacant_list == []:
            select_count = 0

        select_count = int(mutation_change_point)


        select_classes = sample(not_null_result, int(select_count))
        for select in select_classes:
            done = False
            class_id = select['class_id']
            classroom_id = select['classroom_id']
            orig_time_id = select['time_id']

            count = 0

            while not done and len(vacant_list) > 0:
                count += 1
                time_pick_id = choice(vacant_list)
                if time_pick_id <= 32:
                    day_selector = 1
                elif 33 <= time_pick_id <= 47:
                    day_selector = 3
                to_del = f"select * from {offspring_table} where classroom_id = {classroom_id} and class_id={class_id}"
                to_delete = cursor.execute(to_del).fetchall()
                done = offspring_class_assignment(class_id, time_pick_id, classroom_id, day_selector)
                print(done, class_id, classroom_id, time_pick_id)
                if done:
                    print(len(to_delete))
                    for item in to_delete:
                        orig_time_id = item['time_id']
                        print(orig_time_id, class_id, classroom_id)
                        cursor.execute(
                            f"UPDATE {offspring_table} set class_id = NULL where time_id = {orig_time_id} and classroom_id = {classroom_id}")
                    conn.commit()
                if time_pick_id in vacant_list:
                    vacant_list.remove(time_pick_id)
                if count > 50:
                    break
            conn.commit()


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
                                           (classroom_id, time_pick_id, time_pick_id + 5)).fetchall()
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



if __name__ == '__main__':
    consecutive_conflict_class('offspring_0_0')
    mutation("offspring_27_10")
    consecutive_conflict_class('offspring_0_0')
    conn.commit()