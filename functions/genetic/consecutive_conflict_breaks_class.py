import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def consecutive_conflict_class(offspring_table):
    offspring_table_query = f"""select ts.time_id, c.class_id, section_id, day
                                from {offspring_table}
                                    join main.classes c on c.class_id = {offspring_table}.class_id
                                    join main.assign_section_to_class 'aS' on c.class_id = 'aS'.class_id
                                    join main.time_slots ts on {offspring_table}.time_id = ts.time_id
                                order by section_id, {offspring_table}.time_id"""
    offspring_table_res = conn.execute(offspring_table_query)
    # print(offspring_table_query)
    consecutive_count = 0
    previous_section = 1
    previous_time_id = 1
    previous_class = 1
    previous_day = 1
    penalty = 0
    long_breaks = 0
    conflict_count = 0
    for row in offspring_table_res:
        time_id = row['time_id']
        class_id = row['class_id']
        section_id = row['section_id']
        day = row['day']
        if section_id == previous_section:
            if time_id - 1 == previous_time_id and previous_day == day:
                consecutive_count += 1
                # print(f"{time_id}, {previous_time_id},{class_id}, {section_id}")
            elif time_id == previous_time_id:
                # print(section_id, class_id, time_id, previous_time_id,previous_class , previous_section)
                conflict_count += 1
            else:
                consecutive_count = 0
            if day != previous_day:
                consecutive_count = 0
            if previous_day == day:
                if time_id - previous_time_id > 2:
                    long_breaks += 1
            if consecutive_count > 2:

                consecutive_count = 0
                penalty += 1
        else:
            consecutive_count = 0
        previous_section = section_id
        previous_time_id = time_id
        previous_class = class_id
        previous_day = day
    penalty = int(penalty)
    conflict_count = int(conflict_count)
    long_breaks = int(long_breaks)
    print(f"{offspring_table}  |  >3 hour class: {penalty} | conflict: {conflict_count} | long breaks: {long_breaks} |",
          )
    return conflict_count, penalty, long_breaks


if __name__ == '__main__':
    i = 0
    for i in range(4):
        consecutive_conflict_class(f'offspring_0_{i}')

