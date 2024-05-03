import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def first_to_last_class(offspring_table):
    offspring_table_query = f"""select ts.time_id, c.class_id, section_id, day, time_start, time_end
                                from {offspring_table}
                                    join main.classes c on c.class_id = {offspring_table}.class_id
                                    join main.assign_section_to_class 'aS' on c.class_id = 'aS'.class_id
                                    join main.time_slots ts on {offspring_table}.time_id = ts.time_id
                                where time_start = '07:30' or time_start = '07:00' or time_end = '19:30'
                                order by section_id, {offspring_table}.time_id"""
    offspring_table_res = conn.execute(offspring_table_query).fetchall()

    previous_day = 0
    previous_section = 1
    first_to_last = 0
    for row in offspring_table_res:
        time_id = row['time_id']
        class_id = row['class_id']
        section_id = row['section_id']
        day = row['day']
        if previous_day == day and previous_section == section_id:
            first_to_last += 1
        previous_day = day
        previous_section = section_id
    print(f" first to last: {first_to_last}")
    return first_to_last

if __name__ == '__main__':
    first_to_last_class("offspring_0_0")
