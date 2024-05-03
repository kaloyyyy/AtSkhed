import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def tabu_search(offspring_table):

    conn.commit()
    print(f"{color.PURPLE} Tabu Search Started...{color.END}")
    from functions import consecutive_conflict_class
    global check_room_query, update_offspring_table_query, table_name
    table_name = offspring_table
    init_score = consecutive_conflict_class(offspring_table)
    update_offspring_table_query = f'UPDATE {table_name} SET class_id = ? WHERE time_id = ? AND classroom_id = ?'
    check_room_query = (f'select * from {table_name} where classroom_id = ? and time_id >= ? and time_id <= ? '
                        f'and class_id not null')
    offspring_conflict_query = f"""select ts.time_id, c.class_id, day, section_id, c.classroom_id
                                                from {offspring_table}
                                                    join main.classes c on c.class_id = {offspring_table}.class_id
                                                    join main.time_slots ts on {offspring_table}.time_id = ts.time_id
                                                    join main.assign_section_to_class astc on c.class_id = astc.class_id
                                                where c.class_id is not null
                                                order by {offspring_table}.time_id, section_id"""

    offspring_conflict_results = cursor.execute(offspring_conflict_query).fetchall()

    tabu_list = [[False] * 49 for _ in range(69)]
    section_id = offspring_conflict_results[0]['section_id']
    time_id = 0
    conflict = 0
    tries = 0
    orig = init_score = consecutive_conflict_class(offspring_table)
    previous_classroom_id = offspring_conflict_results[0]['classroom_id']
    for result in offspring_conflict_results:
        class_id = result['class_id']
        done = False
        classroom_id = result['classroom_id']
        if section_id == result['section_id']:
            if result['time_id'] == time_id:
                conflict += 1
                # offspring_copy_query = f"""select * from {offspring_table}
                #                     left join main.classes c on c.class_id = {offspring_table}.class_id
                #                     left join main.time_slots ts on {offspring_table}.time_id = ts.time_id
                #                     left join main.assign_section_to_class astc on c.class_id = astc.class_id
                #                     where {offspring_table}.classroom_id = {classroom_id}"""
                # offspring_copy_results = cursor.execute(offspring_copy_query).fetchall()
                # classroom_ids = set(c['classroom_id'] for c in offspring_copy_results)
                # copy_2d_dict = {classroom_id: [] for classroom_id in classroom_ids}
                # for vacant in offspring_copy_results:
                #     time_id = vacant['time_id']
                #     classroom_id = vacant['classroom_id']
                #     copy_2d_dict[classroom_id].append(time_id)

                # print(copy_2d_dict)
                # vacant_2d_array = [copy_2d_dict[classroom_id] for classroom_id in sorted(classroom_ids)]
                c_try = 0
                time_list = list(range(1, 49))
                while not done:  # and c_try < 5:
                    if random() > 0.5:
                        classroom_id = previous_classroom_id
                    else:
                        classroom_id = result['classroom_id']
                    tries += 1
                    c_try += 1
                    if len(time_list) == 0:
                        print(f"{color.PURPLE}----------RAN OUT----------  {color.END}")
                        break
                    # new_rand_time_id = choice(copy_2d_dict[classroom_id])
                    new_rand_time_id = choice(time_list)
                    copy1 = cursor.execute(
                        f"select * from {offspring_table} where time_id = {time_id} and classroom_id = {classroom_id}").fetchall()
                    copy2 = cursor.execute(
                        f"select * from {offspring_table} where time_id = {new_rand_time_id} and classroom_id = {classroom_id}").fetchall()
                    class_id_1 = copy1[0]['class_id']
                    class_id_2 = copy2[0]['class_id']
                    for row1 in copy1:
                        if class_id_2 is None:
                            class_id_2 = "NULL"
                        print(
                            f"update {offspring_table} set class_id = {class_id_2} where time_id = {row1['time_id']} and classroom_id = {row1['classroom_id']}")
                        cursor.execute(
                            f"update {offspring_table} set class_id = {class_id_2} where time_id = {row1['time_id']} and classroom_id = {row1['classroom_id']}")
                    for row2 in copy2:
                        if class_id_1 is None:
                            class_id_1 = "NULL"
                        cursor.execute(
                            f"update {offspring_table} set class_id = {class_id_1} where time_id = {row2['time_id']} and classroom_id = {row2['classroom_id']}")

                    # tabu listed
                    # copy_2d_dict[classroom_id].remove(new_rand_time_id)
                    time_list.remove(new_rand_time_id)
                    new_scores = consecutive_conflict_class(offspring_table)
                    if new_scores[0] < init_score[0]:
                        init_score = new_scores
                        print(f"{color.GREEN}BETTER{color.END}")
                        conn.commit()
                        tries = 0
                        break
                    elif new_scores[0] == init_score[0]:
                        init_score = new_scores
                        print(f"{color.YELLOW}SAME {new_scores[0]}{color.END}")
                        conn.commit()
                    else:
                        conn.rollback()
                        print(f"{color.RED} rollback{color.END}")
                        consecutive_conflict_class(offspring_table)
                    if new_scores[0] < orig[0] - 10:
                        conn.commit()
                        tries = 0
                        init_score = new_scores
                        print(f"{color.CYAN}ORIG{color.END}")
                        break

        if tries == 100:
            break
        previous_classroom_id = classroom_id
        time_id = result['time_id']
        section_id = result['section_id']
    print(conflict)


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
    for i in range(60):
        tabu_search(f'offspring_65_{i}')
