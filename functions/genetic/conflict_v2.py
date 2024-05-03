import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *

def check_conflicts(offspring_table):
    section_query = f"select * from main.sections"
    section_results = cursor.execute(section_query).fetchall()
    conflicts = 0
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
        conflicts += (len(pick_time_list) - len(pick_time_set))
    print(f"conflicts: {conflicts}")
    return conflicts
if __name__ == '__main__':
    for i in range(int(offspring_count)):
        check_conflicts(f"offspring_12"
                        f"_{i}")