import random
import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def hillclimb(offspring_table):

    conn.commit()
    print(f"{color.PURPLE} Hill Climb Search Started... {color.END}")
    from functions import consecutive_conflict_class
    offspring_conflict_query = f"""select ts.time_id, c.class_id, day, section_id, c.classroom_id
                                                from {offspring_table}
                                                    join main.classes c on c.class_id = {offspring_table}.class_id
                                                    join main.time_slots ts on {offspring_table}.time_id = ts.time_id
                                                    join main.assign_section_to_class astc on c.class_id = astc.class_id
                                                where c.class_id is not null
                                                order by {offspring_table}.time_id, section_id"""

    offspring_conflict_results = cursor.execute(offspring_conflict_query).fetchall()
    section_id = offspring_conflict_results[0]['section_id']
    time_id = 0
    conflict = 0
    orig = consecutive_conflict_class(offspring_table)
    init_score = consecutive_conflict_class(offspring_table)
    tries = 0
    for result in offspring_conflict_results:

        class_id = result['class_id']
        done = False
        classroom_id = result['classroom_id']
        if section_id == result['section_id']:
            if result['time_id'] == time_id:
                conflict += 1

                time_list = list(range(1,49))
                c_tries =  0
                while not done and c_tries < 5:
                    tries +=1
                    c_tries +=1
                    select_shuffle_query = f"""select * from {offspring_table} where classroom_id = {classroom_id} order by time_id"""
                    select_shuffle_results = cursor.execute(select_shuffle_query).fetchall()
                    shuffled = sample([row['class_id'] for row in select_shuffle_results],
                                      len(select_shuffle_results))

                    for time_i, row in enumerate(select_shuffle_results):
                        update_query = f"UPDATE {offspring_table} set class_id = ? where classroom_id = ? and time_id = ?"
                        if shuffled[time_i] is None:
                            update_query = f"UPDATE {offspring_table} set class_id = NULL where classroom_id = ? and time_id = ?"
                            cursor.execute(update_query, (classroom_id, row['time_id']))
                        else:
                            cursor.execute(update_query, (shuffled[time_i], classroom_id, row['time_id']))
                    new_scores = consecutive_conflict_class(offspring_table)
                    if new_scores[0] < init_score[0]:
                        init_score = new_scores
                        print(f"{color.GREEN}BETTER {new_scores[0]}{color.END}")
                        conn.commit()
                        break
                    if new_scores[0] == init_score[0]:
                        init_score = new_scores
                        print(f"{color.YELLOW}SAME {new_scores[0]}{color.END}")
                        conn.commit()
                    else:
                        conn.rollback()
                        print(f"{color.RED} rollback{color.END}")
                        new_scores = consecutive_conflict_class(offspring_table)
                    print(new_scores[0], init_score[0])
                    if new_scores[0] <= (orig[0] - 10):
                        print(f"{color.CYAN}ORIG {new_scores[0]}{color.END}")
                        conn.commit()
                        break
        if tries == 50:
            break
        time_id = result['time_id']
        section_id = result['section_id']

if __name__ == '__main__':
    for i in range(4):
        hillclimb(f'offspring_65_5')
