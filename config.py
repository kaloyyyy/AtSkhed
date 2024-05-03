import os.path
import sqlite3
import time
from functools import wraps
import numpy as np
from random import *

import pandas as pd

pd.set_option('display.max_rows', None)  # Set maximum number of rows to display (None means unlimited)
pd.set_option('display.max_columns', None)  # Set maximum number of columns to display (None means unlimited)
pd.set_option('display.max_colwidth', None)  # Set maximum column width to unlimited
pd.set_option('display.expand_frame_repr', False)  # Disable wrapping of the DataFrame

# Display the DataFrame
import string

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Construct the path to the database file (assuming it's in the same directory as the script)
database_file_path = os.path.join(os.path.dirname(current_script_path), 'db/db.sqlite3')

conn = sqlite3.connect(database_file_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

TIME_RES = cursor.execute("select * from time_slots").fetchall()
SETTINGS = cursor.execute("select * from settings").fetchall()
for row in SETTINGS:
    # Access data by column names
    setting_id = row['setting_id']
    setting_name = row['setting_name']
    setting_value = row['setting_value']
    # Create variables here using setting_name and setting_value
    globals()[setting_name] = setting_value
current_sem = semester
prospectus_sem_query = (
    f"""select * from prospectus 
    join main.courses c on c.course_id = prospectus.course_id 
    where semester  = {current_sem} order by c.course_id, program_id""")
# scheduleQuery = "select * from schedule"
programs_query = "select * from programs"
rle_query = "select * from RLE_schedule"

RLE_RES = cursor.execute(rle_query).fetchall()
CLASSROOM_RES = cursor.execute("select * from main.classrooms").fetchall()
PROSPECTUS_RES = cursor.execute(prospectus_sem_query).fetchall()
# SCHEDULE_RES = CUR_DB.execute(scheduleQuery).fetchall()
PROGRAMS_RES = cursor.execute(programs_query).fetchall()
ID_730_START = [2, 27, 52, 77, 102, 127]


# ANSI color codes
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class_query = """select * from classes
                    left join main.classrooms c on classes.classroom_id = c.classroom_id
                    left join main.prospectus p on classes.prospectus_id = p.prospectus_id
                    left join main.courses c2 on p.course_id = c2.course_id"""
CLASS_RES = cursor.execute(class_query).fetchall()

select_assign_section_query = """SELECT c.class_id, s.section_id, program_name, code, section, units, c2.course_id, classroom_id
                            FROM assign_section_to_class
                            JOIN main.classes c ON c.class_id = assign_section_to_class.class_id
                            JOIN main.sections s ON s.section_id = assign_section_to_class.section_id
                            JOIN main.programs p ON p.program_id = s.program_id
                            JOIN main.prospectus p2 ON c.prospectus_id = p2.prospectus_id
                            JOIN main.courses c2 ON p2.course_id = c2.course_id
                            WHERE c.class_id = ?"""

RLE_courses_query = f"select course_id from RLE_courses"
RLE_courses_result = cursor.execute(RLE_courses_query).fetchall()
RLE_courses = [row[0] for row in RLE_courses_result]


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper
