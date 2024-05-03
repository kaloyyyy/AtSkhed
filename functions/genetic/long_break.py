import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def check_long_break(offspring_table):
    section_query = f"select * from main.sections"
    section_results = cursor.execute(section_query).fetchall()
    previous_time_id = 1
    previous_day = 1
    long_breaks = 0
    for section in section_results:
        section_id = section['section_id']
        sched_section_query = f"""select ts.time_id, c.class_id, day
                                                from {offspring_table}
                                                    join main.classes c on c.class_id = {offspring_table}.class_id
                                                    join main.time_slots ts on {offspring_table}.time_id = ts.time_id
                                                    join main.assign_section_to_class astc on c.class_id = astc.class_id
                                                where section_id = {section_id}
                                                order by {offspring_table}.time_id"""
        sched_section_results = cursor.execute(sched_section_query).fetchall()
        pick_time_list = [row["time_id"] for row in sched_section_results]
        pick_time_set = set(pick_time_list)

        for row in sched_section_results:
            time_id = row['time_id']
            day = row['day']

            if previous_day == day:
                if time_id - previous_time_id > 2:
                    long_breaks += 1
            previous_time_id = time_id
            previous_day = day
    # offspring_0_0  |  >3 hour class: 22 | conflict: 224 | long breaks: 278 |
    print(f"long breaks: {long_breaks}")
    return long_breaks

if __name__ == '__main__':
    check_consecutive('offspring_0_0')
