# LOL this one could've done manually, but I decided to do it anyway
import sys
import os

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_dir)

from config import *


def get_RLE_course_id_to_schedule_table():
    RLE_courses_query = ("select * from RLE_courses")
    RLE_schedule_query = ("select * from RLE_schedule")
    nursing_Prosectus_query = ("select * from main.prospectus where program_id = 1")
    RLE_courses_result = cursor.execute(RLE_courses_query).fetchall()
    RLE_schedule_result = cursor.execute(RLE_schedule_query).fetchall()
    Nursing_Prosectus_result = cursor.execute(nursing_Prosectus_query)
    for row in RLE_courses_result:
        ...

if __name__ == '__main__':
    ...
